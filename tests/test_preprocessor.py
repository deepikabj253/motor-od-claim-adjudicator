from app.agent.preprocessor import preprocess_claim


claim_text = """
Customer Name: XXX
Vehicle Number: TN 09 AB 1234
DL Number: DL-1420110012345
VIN: MAT12345678901234

Accident Description:
The insured vehicle was damaged in a road accident.
"""

processed_claim = preprocess_claim(claim_text)

print("Processed Claim:")
print(processed_claim)