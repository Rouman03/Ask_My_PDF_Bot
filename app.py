import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunking import chunk_text
from utils.embeddings import create_vectorstore
from utils.retriever import retrieve_docs
from utils.chatbot import generate_answer


st.set_page_config(
    page_title="Ask My PDF Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* REMOVE DEFAULT STREAMLIT SPACE */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0f172a);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white;
}

/* MAIN TITLE */
.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0;
}

.subtitle {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: -10px;
    margin-bottom: 2rem;
}

/* CHAT BUBBLES */
.stChatMessage {
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
}

/* USER CHAT */
[data-testid="stChatMessageContent"] {
    font-size: 16px;
}

/* INPUT BOX */
.stChatInputContainer {
    background: rgba(15, 23, 42, 0.95);
    border-top: 1px solid rgba(255,255,255,0.08);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* SUCCESS BOX */
.stSuccess {
    border-radius: 14px;
}

/* EXPANDER */
.streamlit-expanderHeader {
    font-size: 16px;
    font-weight: 600;
    color: white;
}

/* SOURCE CHUNKS */
.chunk-box {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

/* HIDE STREAMLIT MENU */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-title">
DocuChat AI
</div>

<div class="subtitle">
Advanced RAG-based Conversational PDF Assistant
</div>
""", unsafe_allow_html=True)


if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:

    st.markdown("## 📂 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.markdown("---")

    st.markdown("""
    ### ✨ Features

    - Advanced RAG Pipeline  
    - Conversational Memory  
    - Semantic Search  
    - Context-aware Responses  
    - Source Chunk Citations  
    """)

    st.markdown("---")

    st.markdown(
        "<center><small>Built with Streamlit + LangChain</small></center>",
        unsafe_allow_html=True
    )


if uploaded_file:

    # PROCESS ONLY ONCE
    if st.session_state.vectorstore is None:

        with st.spinner("⚡ Processing PDF..."):

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

        st.success("✅ PDF processed successfully!")


   
    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)


   
    query = st.chat_input("Ask anything about your PDF...")


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

            with st.expander("📚 View Source Chunks"):

                for i, doc in enumerate(citations):

                    st.markdown(
                        f"""
                        <div class="chunk-box">
                        <h4>Chunk {i+1}</h4>
                        <p>{doc.page_content}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

else:

    st.markdown("""
    <br><br><br>

    <center>

    <h2 style='color:white;'>
    👋 Welcome
    </h2>

    <p style='color:#94a3b8; font-size:18px; width:70%;'>
    Upload a PDF from the sidebar and start chatting with your documents using an advanced RAG-powered AI assistant.
    </p>

    </center>
    """, unsafe_allow_html=True)