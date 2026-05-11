# Ask My PDF Bot

An intelligent PDF Question Answering chatbot built using Python, LangChain, FAISS, and Large Language Models.  
The application allows users to upload PDF documents and ask questions based on the document content using Retrieval-Augmented Generation (RAG).

---

## Features

- Upload and process PDF documents
- Extract text from PDFs
- Split text into meaningful chunks
- Generate embeddings using Sentence Transformers
- Store embeddings in FAISS vector database
- Retrieve relevant document context
- Ask questions and receive AI-generated answers
- Simple and interactive chatbot interface

---

## Technologies Used

- Python
- LangChain
- FAISS
- Sentence Transformers
- OpenRouter API / Groq API
- Streamlit / FastAPI
- PyPDF
- HuggingFace Embeddings

---

## Project Structure

```text
Ask_My_PDF_Bot/
│
├── assets/
├── data/
├── utils/
│   ├── chatbot.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── pdf_loader.py
│   └── retriever.py
│
├── vectorstore/
├── venv/
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

---

## How It Works

### 1. PDF Loading

The uploaded PDF document is loaded and text is extracted.

### 2. Text Chunking

The extracted text is divided into smaller chunks for efficient retrieval.

### 3. Embedding Generation

Text chunks are converted into vector embeddings using Sentence Transformers.

### 4. Vector Storage

Embeddings are stored inside a FAISS vector database.

### 5. Retrieval

Relevant chunks are retrieved based on the user's question.

### 6. Response Generation

The retrieved context is passed to the language model to generate accurate answers.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Ask_My_PDF_Bot.git
```

### Navigate to Project Folder

```bash
cd Ask_My_PDF_Bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory and add:

```env
OPENROUTER_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

---

## Run the Application

```bash
python app.py
```

---

## Future Improvements

- Multi-PDF support
- Chat history
- Better UI design
- Document summarization
- Voice-based interaction
- Cloud deployment

---

## Applications

- Research assistance
- Academic document analysis
- Resume and report querying
- Legal and business document analysis
- Study material assistant

---

## Author

Rouman Syed Nazeer
