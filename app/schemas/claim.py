from typing import Optional

from pydantic import BaseModel


class MotorClaim(BaseModel):
    customer_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    dl_number: Optional[str] = None
    vin: Optional[str] = None
    accident_description: str
    claim_amount: Optional[float] = None


class ClaimAdjudicationResponse(BaseModel):
    decision: str
    reason: str
    policy_evidence: str
    missing_information: str