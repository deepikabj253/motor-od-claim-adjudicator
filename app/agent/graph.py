from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.agent.preprocessor import preprocess_claim
from app.rag.retriever import get_retriever
from app.agent.prompt import build_adjudication_prompt
from app.agent.adjudicator import get_llm
from app.schemas.claim import ClaimAdjudicationResponse


class ClaimState(TypedDict, total=False):
    claim_text: str
    masked_claim: str
    policy_context: str
    result: ClaimAdjudicationResponse


def preprocess_node(state: ClaimState):
    masked_claim = preprocess_claim(
        state["claim_text"]
    )

    return {
        "masked_claim": masked_claim
    }


def retrieve_policy_node(state: ClaimState):
    retriever = get_retriever()

    policy_documents = retriever.invoke(
        state["masked_claim"]
    )

    policy_context = "\n\n".join(
        document.page_content
        for document in policy_documents
    )

    return {
        "policy_context": policy_context
    }


def adjudicate_node(state: ClaimState):
    prompt = build_adjudication_prompt(
        claim_text=state["masked_claim"],
        policy_context=state["policy_context"],
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    adjudication = ClaimAdjudicationResponse.model_validate_json(
        response.content
    )

    return {
        "result": adjudication
    }


def build_claim_graph():
    graph = StateGraph(ClaimState)

    graph.add_node("preprocess", preprocess_node)
    graph.add_node("retrieve_policy", retrieve_policy_node)
    graph.add_node("adjudicate", adjudicate_node)

    graph.set_entry_point("preprocess")

    graph.add_edge("preprocess", "retrieve_policy")
    graph.add_edge("retrieve_policy", "adjudicate")
    graph.add_edge("adjudicate", END)

    return graph.compile()