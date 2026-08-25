from app.pii.recognizer import mask_pii


def preprocess_claim(claim_text: str) -> str:
    """
    Preprocess a raw motor insurance claim.

    Currently:
    - Validates the input
    - Masks personally identifiable information
    """

    if not claim_text or not claim_text.strip():
        raise ValueError("Claim text cannot be empty")

    masked_claim = mask_pii(claim_text)

    return masked_claim