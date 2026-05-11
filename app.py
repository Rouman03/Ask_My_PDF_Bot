import streamlit as st
from utils.pdf_loader import load_pdf
from utils.chunking import chunk_text
from utils.embeddings import create_vectorstore
from utils.retriever import retrieve_docs
from utils.chatbot import generate_answer

st.set_page_config(
    page_title="Ask My PDF Bot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Ask My PDF Bot (Advanced RAG)")
st.caption("Conversational AI PDF Assistant")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Processing PDF..."):

        text = load_pdf(uploaded_file)

        chunks = chunk_text(text)

        vectorstore = create_vectorstore(chunks)

    st.success("PDF processed successfully!")

    query = st.chat_input("Ask anything about your PDF...")

    if query:

        with st.chat_message("user"):
            st.write(query)

        docs = retrieve_docs(vectorstore, query)

        answer, citations = generate_answer(query, docs)

        with st.chat_message("assistant"):
            st.write(answer)

            with st.expander("📚 Source Chunks"):
                for i, doc in enumerate(citations):
                    st.write(f"### Chunk {i+1}")
                    st.write(doc.page_content)