import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from retriever import Retriever


def test_search_finds_relevant_doc(tmp_path):
    (tmp_path / "a.md").write_text("Options let you pass named parameters to commands.")
    (tmp_path / "b.md").write_text("Shell completion works with bash and zsh.")
    r = Retriever(tmp_path)
    assert r.search("shell completion")[0]["source"].endswith("b.md")


def test_no_match_returns_empty(tmp_path):
    (tmp_path / "a.md").write_text("Options let you pass named parameters.")
    assert Retriever(tmp_path).search("zzzzqqq") == []
