from app.schemas.claim import GarageEstimateItem, MotorClaim


def test_valid_motor_claim():
    claim = MotorClaim(
        customer_name="Test Customer",
        vehicle_number="TN01AB1234",
        dl_number="DL1234567890",
        vin="TESTVIN123456",
        accident_description="Vehicle hit a road divider and front bumper was damaged.",
        accident_type="Impact with Object",
        licence_status="Valid",
        vehicle_age="2 years",
        engine_cc="1200",
        policy_type="Comprehensive",
        vehicle_usage="Private",
        zero_dep="Yes",
        engine_protect="No",
        consumables_cover="Yes",
        claim_amount=4500.0,
        garage_estimate=[
            GarageEstimateItem(
                part_name="Front Bumper",
                category="PLASTIC",
                claimed_amount=4500.0,
            )
        ],
    )

    assert claim.customer_name == "Test Customer"
    assert claim.accident_type == "Impact with Object"
    assert claim.claim_amount == 4500.0
    assert len(claim.garage_estimate) == 1

