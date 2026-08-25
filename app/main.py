from fastapi import FastAPI

from app.schemas.claim import (
    MotorClaim,
    ClaimAdjudicationResponse,
)
from app.agent.graph import build_claim_graph


app = FastAPI(
    title="Motor OD Claim Adjudicator",
    description="API for motor insurance claim adjudication",
    version="1.0.0",
)


# Build the LangGraph workflow once when the application starts
claim_graph = build_claim_graph()


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Motor OD Claim Adjudicator",
    }


@app.post(
    "/api/v1/claims/adjudicate",
    response_model=ClaimAdjudicationResponse,
)
def adjudicate(motor_claim: MotorClaim):
    claim_text = motor_claim.model_dump_json()

    result = claim_graph.invoke(
        {
            "claim_text": claim_text
        }
    )

    return result["result"]