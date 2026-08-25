from app.schemas.claim import MotorClaim


claim = MotorClaim(
    customer_name="Ravi Kumar",
    vehicle_number="TN 09 AB 1234",
    dl_number="DL-1420110012345",
    vin="MAT12345678901234",
    accident_description="Vehicle was damaged in a road accident.",
    claim_amount=75000
)

print("Claim created successfully:")
print(claim)

print("\nClaim as dictionary:")
print(claim.model_dump())