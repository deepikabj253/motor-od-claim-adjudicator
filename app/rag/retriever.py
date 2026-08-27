from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

CHROMA_DIR = "data/chroma"


def get_retriever():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma(
        collection_name="motor_policy",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 2}
    )