from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-base-en-v1.5")


class LocalEmbeddings(Embeddings):

    def embed_documents(self, texts):
        return [model.encode(text).tolist() for text in texts]

    def embed_query(self, text):
        return model.encode(text).tolist()


def create_vectorstore(chunks):

    embeddings = LocalEmbeddings()

    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vectorstore