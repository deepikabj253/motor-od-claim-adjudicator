from app.pii.recognizer import mask_pii


claim_text = """
Customer Name: XXX
Vehicle Number: TN 09 AB 1234
DL Number: DL-1420110012345
VIN: MAT12345678901234

Claim Description:
The insured vehicle TN 09 AB 1234 was damaged in an accident.
The driver used DL-1420110012345.
Vehicle VIN is MAT12345678901234.
"""

masked_claim = mask_pii(claim_text)

print("Original Claim:")
print(claim_text)

print("\nMasked Claim:")
print(masked_claim)