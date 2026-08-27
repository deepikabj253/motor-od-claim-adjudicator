
# =========================================================
# IMT Depreciation Rules
# =========================================================

def get_metal_depreciation(vehicle_age: str) -> float:
    """
    Return depreciation percentage for metallic parts
    based on vehicle age.
    """

    depreciation_rules = {
        "0 - 6 Months": 0.0,
        "6 Months - 1 Year": 5.0,
        "1 - 2 Years": 15.0,
        "2 - 5 Years": 25.0,
        "5 - 10 Years": 40.0,
        "Above 10 Years": 50.0,
    }

    return depreciation_rules.get(
        vehicle_age,
        0.0,
    )


def get_depreciation(
    vehicle_age: str,
    category: str,
    zero_dep: str,
) -> float:
    """
    Calculate depreciation based on part category,
    vehicle age and Zero Dep add-on.
    """

    # -----------------------------------------------------
    # Zero Depreciation
    # -----------------------------------------------------

        # -----------------------------------------------------
    # Zero Depreciation
    # -----------------------------------------------------

    if zero_dep == "Yes" and category in [
        "PLASTIC",
        "RUBBER",
        "METAL",
    ]:
        return 0.0


    # -----------------------------------------------------
    # Category-specific rules
    # -----------------------------------------------------

    if category in [
        "GLASS",
        "LABOUR",
        "PAINTING",
        "CONSUMABLE",
    ]:

        return 0.0


    if category in [
        "PLASTIC",
        "RUBBER",
    ]:

        return 50.0


    if category == "METAL":

        return get_metal_depreciation(
            vehicle_age
        )


    return 0.0


# =========================================================
# Calculate Approved Amount
# =========================================================

def calculate_approved_amount(
    claimed_amount: float,
    depreciation_percentage: float,
) -> float:
    """
    Calculate the approved amount after depreciation.
    """

    depreciation_amount = (
        claimed_amount
        * depreciation_percentage
        / 100
    )

    approved_amount = (
        claimed_amount
        - depreciation_amount
    )

    return round(
        approved_amount,
        2,
    )


# =========================================================
# Assess Garage Estimate Item
# =========================================================

def assess_garage_item(
    part_name: str,
    category: str,
    claimed_amount: float,
    vehicle_age: str,
    zero_dep: str,
) -> dict:

    category = category.upper()

    depreciation_percentage = get_depreciation(
        vehicle_age=vehicle_age,
        category=category,
        zero_dep=zero_dep,
    )

    approved_amount = calculate_approved_amount(
        claimed_amount=claimed_amount,
        depreciation_percentage=depreciation_percentage,
    )

    return {
        "part_name": part_name,
        "category": category,
        "claimed_amount": round(
            claimed_amount,
            2,
        ),
        "depreciation_percentage": (
            depreciation_percentage
        ),
        "approved_amount": approved_amount,
    }


# =========================================================
# Calculate Claim Summary
# =========================================================

def calculate_claim_summary(
    items: list,
    compulsory_deductible: float,
) -> dict:

    total_claimed = sum(
        item["claimed_amount"]
        for item in items
    )

    gross_approved = sum(
        item["approved_amount"]
        for item in items
    )

    net_payable = max(
        gross_approved
        - compulsory_deductible,
        0,
    )

    return {
        "total_claimed": round(
            total_claimed,
            2,
        ),
        "gross_approved": round(
            gross_approved,
            2,
        ),
        "compulsory_deductible": round(
            compulsory_deductible,
            2,
        ),
        "net_payable": round(
            net_payable,
            2,
        ),
    }