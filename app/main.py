from fastapi import FastAPI

from app.schemas.claim import (
    MotorClaim,
    ClaimAdjudicationResponse,
)

from app.agent.graph import build_claim_graph


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Motor OD Claim Adjudicator",
    description="API for motor insurance claim adjudication",
    version="1.0.0",
)


# =========================================================
# Build LangGraph Workflow
# =========================================================

# Build the graph once when the application starts.
# The same compiled graph is reused for each request.

claim_graph = build_claim_graph()


# =========================================================
# Health Check
# =========================================================

@app.get("/api/v1/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Motor OD Claim Adjudicator",
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

        # LLM adjudication result
        "adjudication": result["result"],

        # Deterministic IMT calculation
        "assessment": result.get(
            "assessment"
        ),
    }
