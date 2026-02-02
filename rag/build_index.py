import os, json
import faiss
from sentence_transformers import SentenceTransformer
from rag.ingest import load_documents
from rag.chunk import chunk_text

MODEL_NAME = "all-MiniLM-L6-v2"

def build_index(docs_path="data", out_path="indexes"):
    os.makedirs(out_path, exist_ok=True)
    docs = load_documents(docs_path)

    chunks = []
    for d in docs:
        text_chunks = chunk_text(d["text"], chunk_size=800, overlap=150)
        for idx, chunk in enumerate(text_chunks):
            chunks.append({
                "doc": d["doc"],
                "page": d["page"],
                "chunk_id": f"{d['doc']}::p{d['page']}::c{idx}",
                "text": chunk
            })

    if not chunks:
        raise RuntimeError("No text found. Add .pdf/.txt/.md files to the data/ folder and try again.")

    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, os.path.join(out_path, "faiss.index"))
    with open(os.path.join(out_path, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Indexed {len(chunks)} chunks from {len(docs)} document pages/entries.")

if __name__ == "__main__":
    build_index()
