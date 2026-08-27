import requests
import streamlit as st

# =========================================================
# Configuration
# =========================================================

API_URL = "http://127.0.0.1:8000/api/v1/claims/adjudicate"


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Motor OD Claim Adjudicator",
    page_icon="🚗",
    layout="centered",
)


# =========================================================
# Header
# =========================================================

st.title("🚗 Motor OD Claim Adjudicator")

st.write(
    "AI-powered Motor Own Damage Insurance Claim Adjudication"
)

st.divider()


# =========================================================
# Claim Scenarios
# =========================================================

st.subheader("📋 Claim Scenario")


scenario_data = {

    "Front Bumper Accident": {
        "accident_description": (
            "The vehicle hit a road divider and "
            "the front bumper was damaged."
        ),
        "accident_type": "Impact with Object",
        "licence_status": "Valid",
        "part_name": "Front Bumper",
        "category": "PLASTIC",
        "claim_amount": 4500.0,
    },

    "Driving Without Valid Licence": {
        "accident_description": (
            "The vehicle was involved in an accident "
            "and the driver did not have a valid "
            "driving licence."
        ),
        "accident_type": "Collision",
        "licence_status": "Invalid",
        "part_name": "Front Bumper",
        "category": "PLASTIC",
        "claim_amount": 4500.0,
    },

    "Damage Reason Unknown": {
        "accident_description": (
            "The vehicle is damaged but the reason "
            "for the damage is unknown."
        ),
        "accident_type": "Other",
        "licence_status": "Unknown",
        "part_name": "Front Bumper",
        "category": "PLASTIC",
        "claim_amount": 4500.0,
    },

    "Mechanical Breakdown": {
        "accident_description": (
            "The vehicle stopped due to mechanical "
            "failure without an accident."
        ),
        "accident_type": "Other",
        "licence_status": "Valid",
        "part_name": "Engine Sump",
        "category": "METAL",
        "claim_amount": 12000.0,
    },
}


claim_scenario = st.selectbox(
    "Select Claim Scenario",
    list(scenario_data.keys()),
)


selected_scenario = scenario_data[
    claim_scenario
]


# =========================================================
# Customer / Vehicle Details
# =========================================================

st.subheader("👤 Customer & Vehicle")


customer_name = st.text_input(
    "Customer Name",
    value="Demo Customer",
)


vehicle_number = st.text_input(
    "Vehicle Number",
    value="TN01AB1234",
)


dl_number = st.text_input(
    "Driving Licence Number",
    value="DL123456789",
)


vin = st.text_input(
    "VIN",
    value="TESTVIN123",
)


# =========================================================
# Vehicle / Policy Details
# =========================================================

st.subheader("🚘 Vehicle & Policy Details")


vehicle_age_options = [
    "0 - 6 Months",
    "6 Months - 1 Year",
    "1 - 2 Years",
    "2 - 5 Years",
    "5 - 10 Years",
    "Above 10 Years",
]


vehicle_age = st.selectbox(
    "Vehicle Age",
    vehicle_age_options,
)


engine_cc_options = [
    "Up to 1500cc",
    "Above 1500cc",
]


engine_cc = st.selectbox(
    "Engine Capacity",
    engine_cc_options,
)


policy_type_options = [
    "Comprehensive Private Car",
    "Motor Own Damage",
]


policy_type = st.selectbox(
    "Policy Type",
    policy_type_options,
)


vehicle_usage_options = [
    "Private",
    "Commercial",
]


vehicle_usage = st.selectbox(
    "Vehicle Usage",
    vehicle_usage_options,
)


zero_dep = st.selectbox(
    "Zero Depreciation Add-on",
    [
        "No",
        "Yes",
    ],
)


engine_protect = st.selectbox(
    "Engine Protect Add-on",
    [
        "No",
        "Yes",
    ],
)


consumables_cover = st.selectbox(
    "Consumables Cover",
    [
        "No",
        "Yes",
    ],
)


st.divider()


# =========================================================
# Accident Details
# =========================================================

st.subheader("💥 Accident Details")


accident_types = [
    "Collision",
    "Vehicle Overturning",
    "Impact with Object",
    "Fire",
    "Flood",
    "Theft",
    "Other",
]


default_accident_type = selected_scenario[
    "accident_type"
]


accident_type = st.selectbox(
    "Accident Type",
    accident_types,
    index=accident_types.index(
        default_accident_type
    ),
)


licence_statuses = [
    "Valid",
    "Invalid",
    "Unknown",
]


default_licence_status = selected_scenario[
    "licence_status"
]


licence_status = st.selectbox(
    "Driving Licence Status",
    licence_statuses,
    index=licence_statuses.index(
        default_licence_status
    ),
)


accident_description = st.text_area(
    "Accident Description",
    value=selected_scenario[
        "accident_description"
    ],
    height=120,
)


# =========================================================
# Garage Estimate
# =========================================================

st.subheader("🔧 Garage Estimate")


part_options = [
    "Front Bumper",
    "Rear Bumper",
    "Left Fender",
    "Right Fender",
    "Left Headlamp",
    "Right Headlamp",
    "Bonnet",
    "Door",
    "Windshield Glass",
    "Engine Sump",
    "Other",
]


category_options = [
    "PLASTIC",
    "RUBBER",
    "GLASS",
    "METAL",
    "CONSUMABLE",
    "LABOUR",
    "PAINTING",
]


part_name = st.selectbox(
    "Damaged Part",
    part_options,
    index=part_options.index(
        selected_scenario["part_name"]
    )
    if selected_scenario["part_name"]
    in part_options
    else 0,
)


category = st.selectbox(
    "Part Category",
    category_options,
    index=category_options.index(
        selected_scenario["category"]
    )
    if selected_scenario["category"]
    in category_options
    else 0,
)


claimed_amount = st.number_input(
    "Claim Amount (₹)",
    min_value=0.0,
    value=float(
        selected_scenario["claim_amount"]
    ),
    step=500.0,
)


garage_estimate = [
    {
        "part_name": part_name,
        "category": category,
        "claimed_amount": claimed_amount,
    }
]


# =========================================================
# Claim Preview
# =========================================================

st.divider()

st.subheader("🔍 Claim Preview")


preview_col1, preview_col2 = st.columns(2)


with preview_col1:

    st.write(
        f"**Vehicle:** {vehicle_number}"
    )

    st.write(
        f"**Accident:** {accident_type}"
    )

    st.write(
        f"**Part:** {part_name}"
    )


with preview_col2:

    st.write(
        f"**Licence:** {licence_status}"
    )

    st.write(
        f"**Category:** {category}"
    )

    st.write(
        f"**Claim Amount:** ₹{claimed_amount:,.2f}"
    )


st.divider()


# =========================================================
# Adjudicate Claim
# =========================================================

if st.button(
    "🚀 Adjudicate Claim",
    type="primary",
    use_container_width=True,
):

    # -----------------------------------------------------
    # Validate accident description
    # -----------------------------------------------------

    if not accident_description.strip():

        st.error(
            "Please provide the accident description."
        )

    elif not vehicle_number.strip():

        st.error(
            "Please provide the vehicle number."
        )

    else:

        # -------------------------------------------------
        # Build Claim Payload
        # -------------------------------------------------

        claim = {

            # Customer / Vehicle
            "customer_name": (
                customer_name
                or None
            ),

            "vehicle_number": (
                vehicle_number
                or None
            ),

            "dl_number": (
                dl_number
                or None
            ),

            "vin": (
                vin
                or None
            ),

            # Accident
            "accident_description": (
                accident_description
            ),

            "accident_type": (
                accident_type
            ),

            "licence_status": (
                licence_status
            ),

            # Vehicle / Policy
            "vehicle_age": (
                vehicle_age
            ),

            "engine_cc": (
                engine_cc
            ),

            "policy_type": (
                policy_type
            ),

            "vehicle_usage": (
                vehicle_usage
            ),

            # Add-ons
            "zero_dep": (
                zero_dep
            ),

            "engine_protect": (
                engine_protect
            ),

            "consumables_cover": (
                consumables_cover
            ),

            # Claim
            "claim_amount": (
                claimed_amount
            ),

            # Garage Estimate
            "garage_estimate": (
                garage_estimate
            ),
        }


        try:

            # -------------------------------------------------
            # Call FastAPI
            # -------------------------------------------------

            with st.spinner(
                "🔍 Analyzing claim against the policy..."
            ):

                response = requests.post(
                    API_URL,
                    json=claim,
                    timeout=120,
                )


            # =================================================
            # Successful Response
            # =================================================

            if response.status_code == 200:

                result = response.json()


                st.success(
                    "✅ Claim adjudication completed."
                )


                st.divider()


                # =================================================
                # Mem0 Claim History
                # =================================================

                st.subheader(
                    "🧠 Claim History"
                )


                vehicle_id = result.get(
                    "vehicle_id"
                )


                claim_history = result.get(
                    "claim_history",
                    "NONE",
                )


                if vehicle_id:

                    st.caption(
                        f"Memory ID: {vehicle_id}"
                    )


                if (
                    claim_history
                    and claim_history != "NONE"
                ):

                    st.info(
                        claim_history
                    )

                else:

                    st.success(
                        "No previous claim history found."
                    )


                st.divider()


                # =================================================
                # IMT Assessment
                # =================================================

                assessment = result.get(
                    "assessment"
                )


                if assessment:

                    st.subheader(
                        "💰 IMT Loss Assessment"
                    )


                    items = assessment.get(
                        "items",
                        [],
                    )


                    # -------------------------------------------------
                    # Individual Items
                    # -------------------------------------------------

                    for item in items:

                        st.markdown(
                            f"### 🔧 "
                            f"{item.get('part_name', 'Unknown Part')}"
                        )


                        col1, col2, col3 = (
                            st.columns(3)
                        )


                        with col1:

                            st.metric(
                                "Claimed",
                                (
                                    f"₹"
                                    f"{item.get('claimed_amount', 0):,.2f}"
                                ),
                            )


                        with col2:

                            st.metric(
                                "Depreciation",
                                (
                                    f"{item.get('depreciation_percentage', 0)}%"
                                ),
                            )


                        with col3:

                            st.metric(
                                "Approved",
                                (
                                    f"₹"
                                    f"{item.get('approved_amount', 0):,.2f}"
                                ),
                            )


                        st.caption(
                            f"Category: "
                            f"{item.get('category', 'Unknown')}"
                        )


                    # -------------------------------------------------
                    # Financial Summary
                    # -------------------------------------------------

                    summary = assessment.get(
                        "summary",
                        {},
                    )


                    st.subheader(
                        "📊 Financial Summary"
                    )


                    col1, col2 = (
                        st.columns(2)
                    )


                    with col1:

                        st.metric(
                            "Total Claimed",
                            (
                                f"₹"
                                f"{summary.get('total_claimed', 0):,.2f}"
                            ),
                        )


                        st.metric(
                            "Gross Approved",
                            (
                                f"₹"
                                f"{summary.get('gross_approved', 0):,.2f}"
                            ),
                        )


                    with col2:

                        st.metric(
                            "Deductible",
                            (
                                f"₹"
                                f"{summary.get('compulsory_deductible', 0):,.2f}"
                            ),
                        )


                        st.metric(
                            "Net Payable",
                            (
                                f"₹"
                                f"{summary.get('net_payable', 0):,.2f}"
                            ),
                        )


                    st.divider()


                # =================================================
                # Adjudication Result
                # =================================================

                st.subheader(
                    "📊 Adjudication Result"
                )


                adjudication = result.get(
                    "adjudication"
                )


                # -------------------------------------------------
                # Handle Pydantic Response
                # -------------------------------------------------

                if adjudication is not None:

                    if isinstance(
                        adjudication,
                        dict,
                    ):

                        decision = adjudication.get(
                            "decision",
                            "UNKNOWN",
                        )


                        reason = adjudication.get(
                            "reason",
                            "Not provided",
                        )


                        policy_evidence = (
                            adjudication.get(
                                "policy_evidence",
                                "Not provided",
                            )
                        )


                        missing_information = (
                            adjudication.get(
                                "missing_information",
                                "NONE",
                            )
                        )


                        # -------------------------------------------------
                        # Decision
                        # -------------------------------------------------

                        st.subheader(
                            "Decision"
                        )


                        if decision == "APPROVE":

                            st.success(
                                "✅ APPROVE"
                            )


                        elif decision == "REJECT":

                            st.error(
                                "❌ REJECT"
                            )


                        elif (
                            decision
                            == "NEEDS_REVIEW"
                        ):

                            st.warning(
                                "⚠️ NEEDS REVIEW"
                            )


                        else:

                            st.info(
                                decision
                            )


                        # -------------------------------------------------
                        # Reason
                        # -------------------------------------------------

                        st.subheader(
                            "Reason"
                        )


                        st.write(
                            reason
                        )


                        # -------------------------------------------------
                        # Policy Evidence
                        # -------------------------------------------------

                        st.subheader(
                            "Policy Evidence"
                        )


                        st.info(
                            policy_evidence
                        )


                        # -------------------------------------------------
                        # Missing Information
                        # -------------------------------------------------

                        st.subheader(
                            "Missing Information"
                        )


                        if (
                            missing_information
                            == "NONE"
                            or not missing_information
                        ):

                            st.success(
                                "No missing information"
                            )

                        else:

                            st.warning(
                                missing_information
                            )


                    else:

                        st.warning(
                            "Unexpected adjudication response."
                        )


                        st.json(
                            adjudication
                        )


                else:

                    st.warning(
                        "Adjudication result was not returned."
                    )


                    st.json(
                        result
                    )


            # =================================================
            # API Error
            # =================================================

            else:

                st.error(
                    f"❌ API returned status code "
                    f"{response.status_code}"
                )


                try:

                    st.json(
                        response.json()
                    )


                except ValueError:

                    st.write(
                        response.text
                    )


        # =====================================================
        # Connection Error
        # =====================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Unable to connect to FastAPI."
            )


            st.info(
                "Please start FastAPI using:"
            )


            st.code(
                "uvicorn app.main:app --reload "
                "--host 0.0.0.0 --port 8000"
            )


        # =====================================================
        # Timeout
        # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request timed out. "
                "Please try again."
            )


        # =====================================================
        # Request Error
        # =====================================================

        except requests.exceptions.RequestException as exc:

            st.error(
                f"❌ Request failed: {exc}"
            )


        # =====================================================
        # Unexpected Error
        # =====================================================

        except Exception as exc:  # noqa: BLE001

            st.error(
                f"❌ Unexpected error: {exc}"
            )

