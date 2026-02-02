import os, json
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

def _load(index_path="indexes"):
    index = faiss.read_index(os.path.join(index_path, "faiss.index"))
    with open(os.path.join(index_path, "metadata.json"), "r", encoding="utf-8") as f:
        meta = json.load(f)
    model = SentenceTransformer(MODEL_NAME)
    return index, meta, model

def retrieve(query: str, k: int = 5, index_path="indexes"):
    index, meta, model = _load(index_path)
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    _, I = index.search(q_emb, k)

    results = []
    for idx in I[0]:
        if idx == -1:
            continue
        results.append(meta[idx])
    return results
