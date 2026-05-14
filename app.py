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


# SESSION STORAGE
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    # PROCESS ONLY ONCE
    if st.session_state.vectorstore is None:

        with st.spinner("Processing PDF..."):

            text = load_pdf(uploaded_file)

            # DEBUG
            print("TEXT LENGTH:", len(text))

            if len(text.strip()) == 0:
                st.error("Could not extract text from PDF.")
                st.stop()

            chunks = chunk_text(text)

            print("TOTAL CHUNKS:", len(chunks))

            vectorstore = create_vectorstore(chunks)

            st.session_state.vectorstore = vectorstore

        st.success("PDF processed successfully!")


    query = st.chat_input("Ask anything about your PDF...")


    # DISPLAY OLD CHATS
    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)


    if query:

        st.session_state.chat_history.append(("user", query))

        with st.chat_message("user"):
            st.write(query)

        docs = retrieve_docs(
            st.session_state.vectorstore,
            query
        )

        print("RETRIEVED DOCS:", len(docs))

        answer, citations = generate_answer(
    query,
    docs,
    st.session_state.chat_history
)

        st.session_state.chat_history.append(
            ("assistant", answer)
        )

        with st.chat_message("assistant"):

            st.write(answer)

            with st.expander("📚 Source Chunks"):

                for i, doc in enumerate(citations):

                    st.write(f"### Chunk {i+1}")

                    st.write(doc.page_content)