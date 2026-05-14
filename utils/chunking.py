from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = text_splitter.split_text(text)

    return chunks