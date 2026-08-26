from fastapi import FastAPI

from app.agent.graph import build_claim_graph
from app.schemas.claim import MotorClaim


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Motor OD Claim Adjudicator",
    description=(
        "AI-powered Motor Own Damage Insurance "
        "Claim Adjudication"
    ),
    version="1.0.0",
)


# =========================================================
# Build Claim Graph
# =========================================================

claim_graph = build_claim_graph()


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Motor OD Claim Adjudicator",
    }


# =========================================================
# Root
# =========================================================

@app.get("/")
def root():

    return {
        "service": "Motor OD Claim Adjudicator",
        "status": "running",
    }


# =========================================================
# Claim Adjudication
# =========================================================

@app.post("/api/v1/claims/adjudicate")
def adjudicate(
    motor_claim: MotorClaim,
):

    # -----------------------------------------------------
    # Convert Pydantic claim into JSON
    # -----------------------------------------------------

    claim_text = motor_claim.model_dump_json()

    # -----------------------------------------------------
    # Execute LangGraph
    # -----------------------------------------------------

    result = claim_graph.invoke(
        {
            "claim_text": claim_text
        }
    )

    # -----------------------------------------------------
    # Return complete response
    # -----------------------------------------------------

    return {
        "status": "success",

        # -------------------------------------------------
        # LLM adjudication result
        # -------------------------------------------------

        "adjudication": result.get(
            "result"
        ),

        # -------------------------------------------------
        # Deterministic IMT calculation
        # -------------------------------------------------

        "assessment": result.get(
            "assessment"
        ),

        # -------------------------------------------------
        # Anonymized vehicle memory ID
        # -------------------------------------------------

        "vehicle_id": result.get(
            "vehicle_id"
        ),

        # -------------------------------------------------
        # Previous claim history retrieved from Mem0
        # -------------------------------------------------

        "claim_history": result.get(
            "claim_history",
            "NONE",
        ),
    }
