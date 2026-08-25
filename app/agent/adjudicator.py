import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.agent.prompt import build_adjudication_prompt
from app.rag.retriever import get_retriever


load_dotenv()


def get_llm():
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    temperature = float(os.getenv("TEMPERATURE", "0"))

    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
    )


def adjudicate_claim(claim_text: str) -> str:
    retriever = get_retriever()

    policy_documents = retriever.invoke(claim_text)

    policy_context = "\n\n".join(
        document.page_content
        for document in policy_documents
    )

    prompt = build_adjudication_prompt(
        claim_text=claim_text,
        policy_context=policy_context,
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content