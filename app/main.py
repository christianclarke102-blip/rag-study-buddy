import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from rag.build_index import build_index
from rag.retrieve import retrieve
from rag.generate import generate_answer


st.set_page_config(page_title="RAG Study Buddy", layout="wide")
st.title("📚 RAG Study Buddy (Offline)")

st.sidebar.header("Controls")
if st.sidebar.button("Rebuild Index"):
    build_index()
    st.sidebar.success("Index rebuilt!")

question = st.text_input("Ask a question about your documents:")

if question:
    with st.spinner("Retrieving sources..."):
        sources = retrieve(question, k=5)

    with st.spinner("Generating answer..."):
        answer = generate_answer(question, sources)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Sources used"):
        for i, s in enumerate(sources):
            st.markdown(f"**[{i+1}] {s['doc']} (page {s['page']})**")
            st.write(s["text"][:600] + "...")
