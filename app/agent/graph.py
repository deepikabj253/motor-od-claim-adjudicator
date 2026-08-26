import hashlib
import json
from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.agent.preprocessor import preprocess_claim
from app.rag.retriever import get_retriever
from app.memory.memory import (
    search_claim_memory,
    add_adjudicated_claim_memory,
)
from app.agent.prompt import build_adjudication_prompt
from app.agent.adjudicator import get_llm
from app.schemas.claim import ClaimAdjudicationResponse


# =========================================================
# Claim State
# =========================================================

class ClaimState(TypedDict, total=False):

    claim_text: str

    masked_claim: str

    vehicle_id: str

    claim_history: str

    policy_context: str

    result: ClaimAdjudicationResponse


# =========================================================
# Generate Vehicle Memory ID
# =========================================================

def generate_vehicle_memory_id(
    claim_text: str,
) -> str:
    """
    Generate a deterministic anonymized Mem0 user ID
    from the vehicle number.

    The actual vehicle number is never used as the
    Mem0 user ID.
    """

    try:

        claim_data = json.loads(
            claim_text
        )

        vehicle_number = claim_data.get(
            "vehicle_number"
        )

        if not vehicle_number:

            return "unknown_vehicle"

        normalized_vehicle = (
            vehicle_number
            .strip()
            .upper()
            .replace(" ", "")
            .replace("-", "")
        )

        vehicle_hash = hashlib.sha256(
            normalized_vehicle.encode("utf-8")
        ).hexdigest()[:16]

        return f"vehicle_{vehicle_hash}"

    except (
        json.JSONDecodeError,
        TypeError,
    ):

        return "unknown_vehicle"


# =========================================================
# Preprocess Claim
# =========================================================

def preprocess_node(
    state: ClaimState,
):

    masked_claim = preprocess_claim(
        state["claim_text"]
    )

    vehicle_id = generate_vehicle_memory_id(
        state["claim_text"]
    )

    return {
        "masked_claim": masked_claim,
        "vehicle_id": vehicle_id,
    }


# =========================================================
# Retrieve Claim Memory
# =========================================================

def retrieve_memory_node(
    state: ClaimState,
):

    vehicle_id = state.get(
        "vehicle_id",
        "unknown_vehicle",
    )

    if vehicle_id == "unknown_vehicle":

        return {
            "claim_history": "NONE"
        }

    memories = search_claim_memory(
        vehicle_id=vehicle_id,
        query=(
            "previous claims, vehicle damage history, "
            "NCB history"
        ),
    )

    results = memories.get(
        "results",
        [],
    )

    if results:

        claim_history = "\n\n".join(
            memory.get(
                "memory",
                "",
            )
            for memory in results
            if memory.get("memory")
        )

    else:

        claim_history = "NONE"

    return {
        "claim_history": claim_history
    }


# =========================================================
# Retrieve Policy
# =========================================================

def retrieve_policy_node(
    state: ClaimState,
):

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
# Adjudicate Claim
# =========================================================

def adjudicate_node(
    state: ClaimState,
):

    prompt = build_adjudication_prompt(
        claim_text=state["masked_claim"],
        policy_context=state["policy_context"],
        claim_history=state.get(
            "claim_history",
            "NONE",
        ),
    )

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
# Store Current Claim in Mem0
# =========================================================

def store_claim_memory_node(
    state: ClaimState,
):

    vehicle_id = state.get(
        "vehicle_id",
        "unknown_vehicle",
    )

    if vehicle_id == "unknown_vehicle":

        return {}

    try:

        claim_data = json.loads(
            state["claim_text"]
        )

        claim_description = claim_data.get(
            "accident_description",
            "Motor own damage claim",
        )

        claim_amount = float(
            claim_data.get(
                "claim_amount",
                0,
            )
            or 0
        )

        adjudication = state.get(
            "result"
        )

        if adjudication:

            decision = adjudication.decision

            add_adjudicated_claim_memory(
                vehicle_id=vehicle_id,
                claim_description=claim_description,
                claim_amount=claim_amount,
                decision=decision,
            )

    except Exception as exc:

        print(
            f"Warning: Unable to store claim memory: {exc}"
        )

    return {}


# =========================================================
# Build Claim Graph
# =========================================================

def build_claim_graph():

    graph = StateGraph(
        ClaimState
    )

    # -----------------------------------------------------
    # Nodes
    # -----------------------------------------------------

    graph.add_node(
        "preprocess",
        preprocess_node,
    )

    graph.add_node(
        "retrieve_memory",
        retrieve_memory_node,
    )

    graph.add_node(
        "retrieve_policy",
        retrieve_policy_node,
    )

    graph.add_node(
        "adjudicate",
        adjudicate_node,
    )

    graph.add_node(
        "store_claim_memory",
        store_claim_memory_node,
    )

    # -----------------------------------------------------
    # Entry Point
    # -----------------------------------------------------

    graph.set_entry_point(
        "preprocess"
    )

    # -----------------------------------------------------
    # Workflow
    # -----------------------------------------------------

    graph.add_edge(
        "preprocess",
        "retrieve_memory",
    )

    graph.add_edge(
        "retrieve_memory",
        "retrieve_policy",
    )

    graph.add_edge(
        "retrieve_policy",
        "adjudicate",
    )

    graph.add_edge(
        "adjudicate",
        "store_claim_memory",
    )

    graph.add_edge(
        "store_claim_memory",
        END,
    )

    # -----------------------------------------------------
    # Compile
    # -----------------------------------------------------

    return graph.compile()
