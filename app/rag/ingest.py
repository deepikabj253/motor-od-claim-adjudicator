from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


load_dotenv()


POLICY_DIR = Path("data/policies")
CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "motor_policy"


def load_policy_documents():
    documents = []

    for file_path in POLICY_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name
                }
            )
        )

    return documents


def create_vector_store():
    documents = load_policy_documents()

    if not documents:
        raise ValueError("No policy documents found.")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    document_ids = [
        document.metadata["source"]
        for document in documents
    ]

    vector_store.add_documents(
        documents=documents,
        ids=document_ids,
    )

    return vector_store