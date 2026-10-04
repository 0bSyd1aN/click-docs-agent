# Click Docs Agent

A small RAG agent that answers questions about the Click docs.

- `retriever.py`: chunks `.md`/`.rst` files and ranks chunks with TF-IDF cosine similarity
- `agent.py`: tool-use loop. Claude calls `search_docs`, reads the passages, and answers with source citations. Capped at 5 steps.
- No API key set: falls back to retrieval-only mode
- `tests/`: pytest for the retriever

## Run

    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...   # optional
    python agent.py "How do I add a required option?"
    pytest -q

Docs are copied from pallets/click (BSD-3-Clause).
