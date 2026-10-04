import os
import sys

from retriever import Retriever

TOOLS = [{
    "name": "search_docs",
    "description": "Search the documentation. Returns top passages with source paths.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
}]
SYSTEM = "Answer using only the docs via search_docs. Cite source paths. If the docs do not cover it, say so."


def run_tool(retriever, query):
    hits = retriever.search(query)
    return "\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits) or "No results."


def ask(question, retriever, max_steps=5):
    import anthropic

    client = anthropic.Anthropic()
    msgs = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        resp = client.messages.create(
            model=os.getenv("MODEL", "claude-sonnet-5-5"),
            max_tokens=1000,
            system=SYSTEM,
            tools=TOOLS,
            messages=msgs,
        )
        msgs.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        results = [
            {"type": "tool_result", "tool_use_id": b.id, "content": run_tool(retriever, b.input["query"])}
            for b in resp.content
            if b.type == "tool_use"
        ]
        msgs.append({"role": "user", "content": results})
    return "Stopped: step limit reached."


if __name__ == "__main__":
    r = Retriever(os.getenv("DOCS_DIR", "docs"))
    q = " ".join(sys.argv[1:]) or "How do I add a required option?"
    if os.getenv("ANTHROPIC_API_KEY"):
        print(ask(q, r))
    else:
        print("No ANTHROPIC_API_KEY set: retrieval-only mode.\n")
        print(run_tool(r, q))
