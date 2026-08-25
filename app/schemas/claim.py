from typing import Optional, List

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

    customer_name: Optional[str] = None

    vehicle_number: Optional[str] = None

    dl_number: Optional[str] = None

    vin: Optional[str] = None

    # -----------------------------------------------------
    # Accident Information
    # -----------------------------------------------------

    accident_description: str

    accident_type: Optional[str] = None

    licence_status: Optional[str] = None

    # -----------------------------------------------------
    # Vehicle / Policy Information
    # -----------------------------------------------------

    vehicle_age: Optional[str] = None

    engine_cc: Optional[str] = None

    policy_type: Optional[str] = None

    vehicle_usage: Optional[str] = None

    # -----------------------------------------------------
    # Add-on Covers
    # -----------------------------------------------------

    zero_dep: Optional[str] = "No"

    engine_protect: Optional[str] = "No"

    consumables_cover: Optional[str] = "No"

    # -----------------------------------------------------
    # Claim Amount
    # -----------------------------------------------------

    claim_amount: Optional[float] = None

    # -----------------------------------------------------
    # Garage Estimate
    # -----------------------------------------------------

    garage_estimate: List[GarageEstimateItem] = Field(
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
