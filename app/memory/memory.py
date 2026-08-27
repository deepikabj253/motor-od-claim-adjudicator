import os

from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()


def get_memory():
    """
    Create and return the Mem0 memory client.
    """

    config = {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "motor_claim_memory",
                "path": "data/memory",
            },
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": os.getenv(
                    "OPENAI_MODEL_NAME",
                    "gpt-4o-mini",
                ),
                "temperature": 0,
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
            },
        },
    }

    return Memory.from_config(config)


def add_claim_memory(
    vehicle_id: str,
    claim_text: str,
):
    """
    Store anonymized claim history in Mem0.
    """

    memory = get_memory()

    memory.add(
        claim_text,
        user_id=vehicle_id,
    )


def search_claim_memory(
    vehicle_id: str,
    query: str,
):
    """
    Retrieve relevant historical claim information.
    """

    memory = get_memory()

    result = memory.search(
    query,
    filters={"user_id": vehicle_id},
    )

    return result

def add_adjudicated_claim_memory(
    vehicle_id: str,
    claim_description: str,
    claim_amount: float,
    decision: str,
) -> None:
    """
    Store the current adjudicated claim in Mem0.
    """

    if not vehicle_id:
        return

    if vehicle_id == "unknown_vehicle":
        return

    memory_text = (
        f"Vehicle had a motor own damage claim. "
        f"Incident: {claim_description}. "
        f"Claim amount: ₹{claim_amount:.2f}. "
        f"Adjudication decision: {decision}."
    )

    # Get the initialized Mem0 instance
    memory = get_memory()

    memory.add(
        memory_text,
        user_id=vehicle_id,
    )