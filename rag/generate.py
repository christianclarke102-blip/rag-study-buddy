import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

def generate_answer(question: str, sources: list):
    context = "\n\n".join(
        [f"[{i+1}] ({s['doc']} p{s['page']}) {s['text']}" for i, s in enumerate(sources)]
    )

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the sources below.
If the sources do not contain the answer, say: "I don't have enough information in the documents to answer that."
Always include citations like [1], [2] at the end of sentences.

SOURCES:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False})
    r.raise_for_status()
    return r.json()["response"]
