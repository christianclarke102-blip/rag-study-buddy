import os
from pypdf import PdfReader

def load_documents(docs_path="data"):
    docs = []
    for root, _, files in os.walk(docs_path):
        for f in files:
            path = os.path.join(root, f)

            if f.lower().endswith(".pdf"):
                reader = PdfReader(path)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    docs.append({"doc": f, "page": i + 1, "text": text})

            elif f.lower().endswith((".txt", ".md")):
                with open(path, "r", encoding="utf-8") as fp:
                    docs.append({"doc": f, "page": None, "text": fp.read()})

    return docs
