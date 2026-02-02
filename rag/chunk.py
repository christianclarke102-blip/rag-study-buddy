def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    text = text.replace("\n", " ").strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += max(chunk_size - overlap, 1)
    return chunks
