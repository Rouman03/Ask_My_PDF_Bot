def retrieve_docs(vectorstore, query):

    docs = vectorstore.similarity_search(query, k=4)

    return docs