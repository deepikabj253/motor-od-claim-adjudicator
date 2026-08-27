from app.tools.imt_calculator import (
    assess_garage_item,
    calculate_approved_amount,
    calculate_claim_summary,
    get_depreciation,
)


def test_metal_depreciation():
    depreciation = get_depreciation(
        vehicle_age="2 - 5 Years",
        category="METAL",
        zero_dep="No",
    )

    assert depreciation == 25.0


def test_zero_depreciation():
    depreciation = get_depreciation(
        vehicle_age="2 - 5 Years",
        category="METAL",
        zero_dep="Yes",
    )

    assert depreciation == 0.0


def test_approved_amount():
    approved = calculate_approved_amount(
        claimed_amount=10000.0,
        depreciation_percentage=25.0,
    )

    assert approved == 7500.0


def test_assess_garage_item():
    result = assess_garage_item(
        part_name="Engine Sump",
        category="METAL",
        claimed_amount=12000.0,
        vehicle_age="2 - 5 Years",
        zero_dep="No",
    )

    assert result["part_name"] == "Engine Sump"
    assert result["category"] == "METAL"
    assert result["depreciation_percentage"] == 25.0
    assert result["approved_amount"] == 9000.0


def test_claim_summary():
    items = [
        {
            "claimed_amount": 12000.0,
            "approved_amount": 9000.0,
        },
        {
            "claimed_amount": 4500.0,
            "approved_amount": 4500.0,
        },
    ]

    result = calculate_claim_summary(
        items=items,
        compulsory_deductible=1000.0,
    )

    assert result["total_claimed"] == 16500.0
    assert result["gross_approved"] == 13500.0
    assert result["compulsory_deductible"] == 1000.0
    assert result["net_payable"] == 12500.0
