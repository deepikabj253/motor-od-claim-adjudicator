
from pydantic import BaseModel, Field

# =========================================================
# Garage Estimate Item
# =========================================================

class GarageEstimateItem(BaseModel):
    """
    Represents one item from the garage repair estimate.
    """

    part_name: str

    category: str

    claimed_amount: float


# =========================================================
# Motor Claim
# =========================================================

class MotorClaim(BaseModel):
    """
    Input schema for a Motor Own Damage insurance claim.
    """

    # -----------------------------------------------------
    # Customer / Vehicle Information
    # -----------------------------------------------------

    customer_name: str | None = None

    vehicle_number: str | None = None

    dl_number: str | None = None

    vin: str | None = None

    # -----------------------------------------------------
    # Accident Information
    # -----------------------------------------------------

    accident_description: str

    accident_type: str | None = None

    licence_status: str | None = None

    # -----------------------------------------------------
    # Vehicle / Policy Information
    # -----------------------------------------------------

    vehicle_age: str | None = None

    engine_cc: str | None = None

    policy_type: str | None = None

    vehicle_usage: str | None = None

    # -----------------------------------------------------
    # Add-on Covers
    # -----------------------------------------------------

    zero_dep: str | None = "No"

    engine_protect: str | None = "No"

    consumables_cover: str | None = "No"

    # -----------------------------------------------------
    # Claim Amount
    # -----------------------------------------------------

    claim_amount: float | None = None

    # -----------------------------------------------------
    # Garage Estimate
    # -----------------------------------------------------

    garage_estimate: list[GarageEstimateItem] = Field(
        default_factory=list
    )


# =========================================================
# Adjudication Response
# =========================================================

class ClaimAdjudicationResponse(BaseModel):
    """
    Structured response returned by the adjudication agent.
    """

    decision: str

    reason: str

    policy_evidence: str

    missing_information: str
