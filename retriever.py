from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_chunks(root, size=800):
    chunks = []
    for p in sorted(Path(root).rglob("*")):
        if p.suffix in {".md", ".rst"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for i in range(0, len(text), size):
                piece = text[i : i + size].strip()
                if piece:
                    chunks.append({"source": str(p), "text": piece})
    return chunks


class Retriever:
    def __init__(self, root):
        self.chunks = load_chunks(root)
        self.vec = TfidfVectorizer(stop_words="english")
        self.matrix = self.vec.fit_transform([c["text"] for c in self.chunks])

    def search(self, query, k=4):
        scores = cosine_similarity(self.vec.transform([query]), self.matrix)[0]
        top = scores.argsort()[::-1][:k]
        return [{**self.chunks[i], "score": float(scores[i])} for i in top if scores[i] > 0]
