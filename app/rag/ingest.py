from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


POLICY_DIR = Path("data/policies")
CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "motor_policy"


def load_policy_documents():
    documents = []

    for file_path in POLICY_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name
                },
            )
        )

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


def create_vector_store():

    documents = load_policy_documents()

    if not documents:
        raise ValueError(
            "No policy documents found."
        )

    # -----------------------------------------------------
    # Chunk policy documents
    # -----------------------------------------------------

    chunks = split_documents(
        documents
    )

    print(
        f"Loaded documents: {len(documents)}"
    )

    print(
        f"Created chunks: {len(chunks)}"
    )

    # -----------------------------------------------------
    # Embeddings
    # -----------------------------------------------------

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # -----------------------------------------------------
    # ChromaDB
    # -----------------------------------------------------

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # -----------------------------------------------------
    # Add chunks
    # -----------------------------------------------------

    vector_store.add_documents(
        documents=chunks
    )

    print(
        "Policy chunks successfully stored in ChromaDB."
    )

    return vector_store


if __name__ == "__main__":

    create_vector_store()