from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.agent.preprocessor import preprocess_claim
from app.rag.retriever import get_retriever
from app.agent.prompt import build_adjudication_prompt
from app.agent.adjudicator import get_llm
from app.schemas.claim import ClaimAdjudicationResponse
from app.tools.imt_calculator import assess_garage_item, calculate_claim_summary


class ClaimState(TypedDict, total=False):

    claim_text: str

    masked_claim: str

    policy_context: str

    assessment: dict

    result: ClaimAdjudicationResponse


# =========================================================
# PII Preprocessing
# =========================================================

def preprocess_node(state: ClaimState):

    masked_claim = preprocess_claim(
        state["claim_text"]
    )

    return {
        "masked_claim": masked_claim
    }


# =========================================================
# Policy Retrieval
# =========================================================

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


# =========================================================
# IMT Assessment
# =========================================================

def calculate_assessment_node(
    state: ClaimState
):

    claim = state["claim_text"]

    import json

    claim_data = json.loads(
        claim
    )

    vehicle_age = claim_data.get(
        "vehicle_age",
        "0 - 6 Months",
    )

    zero_dep = claim_data.get(
        "zero_dep",
        "No",
    )

    garage_estimate = claim_data.get(
        "garage_estimate",
        [],
    )

    assessed_items = []

    for item in garage_estimate:

        assessed_item = assess_garage_item(
            part_name=item["part_name"],
            category=item["category"],
            claimed_amount=item["claimed_amount"],
            vehicle_age=vehicle_age,
            zero_dep=zero_dep,
        )

        assessed_items.append(
            assessed_item
        )

    # -----------------------------------------------------
    # Deductible
    # -----------------------------------------------------

    compulsory_deductible = 1000.0

    summary = calculate_claim_summary(
        items=assessed_items,
        compulsory_deductible=compulsory_deductible,
    )

    assessment = {
        "items": assessed_items,
        "summary": summary,
    }

    return {
        "assessment": assessment
    }


# =========================================================
# Adjudication
# =========================================================

def adjudicate_node(
    state: ClaimState
):

    prompt = build_adjudication_prompt(
        claim_text=state["masked_claim"],
        policy_context=state["policy_context"],
    )

    # Add deterministic IMT calculation
    prompt += f"""

IMT ASSESSMENT:

{state["assessment"]}

IMPORTANT:
The IMT assessment above was calculated by deterministic
Python logic.

Do not recalculate these values.
Use them when explaining the financial assessment.
"""

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    adjudication = (
        ClaimAdjudicationResponse
        .model_validate_json(
            response.content
        )
    )

    return {
        "result": adjudication
    }


# =========================================================
# Build LangGraph
# =========================================================

def build_claim_graph():

    graph = StateGraph(
        ClaimState
    )

    graph.add_node(
        "preprocess",
        preprocess_node,
    )

    graph.add_node(
        "retrieve_policy",
        retrieve_policy_node,
    )

    graph.add_node(
        "calculate_assessment",
        calculate_assessment_node,
    )

    graph.add_node(
        "adjudicate",
        adjudicate_node,
    )

    graph.set_entry_point(
        "preprocess"
    )

    graph.add_edge(
        "preprocess",
        "retrieve_policy",
    )

    graph.add_edge(
        "retrieve_policy",
        "calculate_assessment",
    )

    graph.add_edge(
        "calculate_assessment",
        "adjudicate",
    )

    graph.add_edge(
        "adjudicate",
        END,
    )

    return graph.compile()