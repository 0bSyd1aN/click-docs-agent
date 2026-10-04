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

## How it works

1. `Retriever` splits each doc into 800-character chunks and builds a TF-IDF matrix.
2. The model gets one tool, `search_docs`. It calls it with a query and receives the top 4 chunks with their source paths.
3. The loop repeats until the model answers or hits the 5-step cap.

## Limitations

- TF-IDF matches keywords, not meaning. Embeddings would handle paraphrased questions better.
- Fixed-size chunks can cut a section in half.
- No evaluation set yet to measure answer quality.
