from app.agent.adjudicator import adjudicate_claim


claim = """
Customer Name: XXX
Vehicle Number: <INDIAN_RC>
DL Number: <INDIAN_DL>
VIN: <VEHICLE_VIN>

The insured vehicle was damaged in a road accident.
The vehicle collided with another vehicle.
"""


result = adjudicate_claim(claim)

print("Claim Adjudication Result:")
print(result)