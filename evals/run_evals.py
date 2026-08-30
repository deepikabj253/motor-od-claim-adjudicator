import os
from typing import Any

from langchain_openai import ChatOpenAI
from langsmith import Client

from app.agent.graph import build_claim_graph
from app.schemas.claim import MotorClaim

# =========================================================
# Configuration
# =========================================================

LANGSMITH_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT",
    "motor-od-claim-adjudicator-evals",
)

LANGSMITH_API_KEY = os.getenv("LANGCHAIN_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = Client()


# =========================================================
# Evaluation Cases
# =========================================================

EVALUATION_CASES = [
    {
        "name": "Covered accidental damage",
        "inputs": {
            "claim": MotorClaim(
                customer_name="Test Customer",
                vehicle_number="TN01AB1234",
                accident_description=(
                    "Vehicle hit a road divider and the "
                    "front bumper was damaged."
                ),
                accident_type="Accident",
                licence_status="Valid",
                vehicle_age="2 years",
                engine_cc="1200",
                policy_type="Comprehensive",
                vehicle_usage="Private",
                zero_dep="Yes",
                engine_protect="No",
                consumables_cover="Yes",
                claim_amount=4500,
            ).model_dump_json(),
        },
        "reference": {
            "decision": "APPROVE",
        },
    },
    {
        "name": "Missing licence information",
        "inputs": {
            "claim": MotorClaim(
                customer_name="Test Customer",
                vehicle_number="TN02CD5678",
                accident_description=(
                    "Vehicle was damaged in an accident."
                ),
                accident_type="Accident",
                licence_status=None,
                vehicle_age="3 years",
                engine_cc="1200",
                policy_type="Comprehensive",
                vehicle_usage="Private",
                zero_dep="No",
                engine_protect="No",
                consumables_cover="No",
                claim_amount=6000,
            ).model_dump_json(),
        },
        "reference": {
            "decision": "APPROVE",
        },
    },
]


# =========================================================
# Motor OD Claim Application
# =========================================================

def run_claim(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Execute the complete Motor OD claim adjudication graph.
    """

    graph = build_claim_graph()

    result = graph.invoke(
        {
            "claim_text": inputs["claim"],
        }
    )

    adjudication = result.get("result")

    if adjudication is None:
        raise RuntimeError(
            "Claim graph did not return an adjudication result."
        )

    return {
        "decision": adjudication.decision,
        "reason": adjudication.reason,
        "policy_evidence": adjudication.policy_evidence,
        "missing_information": (
            adjudication.missing_information
        ),
        "assessment": result.get("assessment"),
        "claim_history": result.get(
            "claim_history",
            "NONE",
        ),
        "vehicle_id": result.get(
            "vehicle_id",
        ),
    }


# =========================================================
# LLM-as-a-Judge
# =========================================================

judge_llm = ChatOpenAI(
    model=os.getenv(
        "LANGSMITH_JUDGE_MODEL",
        "gpt-4o-mini",
    ),
    temperature=0,
)


def llm_judge(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    """
    LLM-as-a-Judge evaluator.

    The judge verifies whether the claim adjudication
    decision matches the expected decision and whether
    the reasoning is consistent with the case.
    """

    actual_decision = str(
        outputs.get("decision", "")
    ).upper()

    expected_decision = str(
        reference_outputs.get("decision", "")
    ).upper()

    reason = outputs.get(
        "reason",
        "",
    )

    prompt = f"""
You are an expert Motor Own Damage insurance
claim adjudication evaluator.

Evaluate the following claim adjudication result.

Expected decision:
{expected_decision}

Actual decision:
{actual_decision}

Adjudication reason:
{reason}

Evaluation criteria:

1. The actual decision must match the expected decision.
2. The reasoning must be consistent with the expected
   decision.
3. The reasoning must not contradict the claim information.

Return ONLY one word:

PASS

if the result is correct.

Otherwise return:

FAIL
"""

    response = judge_llm.invoke(prompt)

    judge_result = response.content.strip().upper()

    passed = judge_result == "PASS"

    return {
        "key": "llm_judge",
        "score": 1 if passed else 0,
        "value": "PASS" if passed else "FAIL",
        "comment": (
            f"Expected={expected_decision}, "
            f"Actual={actual_decision}"
        ),
    }


# =========================================================
# Deterministic Decision Evaluator
# =========================================================

def decision_evaluator(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    """
    Deterministic evaluator used as an additional
    safety check for the CI/CD gate.
    """

    actual = str(
        outputs.get("decision", "")
    ).upper()

    expected = str(
        reference_outputs.get("decision", "")
    ).upper()

    passed = actual == expected

    return {
        "key": "decision_accuracy",
        "score": 1 if passed else 0,
        "value": "PASS" if passed else "FAIL",
        "comment": (
            f"Expected={expected}, "
            f"Actual={actual}"
        ),
    }


# =========================================================
# Evaluation Target
# =========================================================

def target(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Target function passed to LangSmith evaluate().
    """

    return run_claim(inputs)


# =========================================================
# Main Evaluation
# =========================================================

def run_evaluation() -> None:
    """
    Execute the Motor OD evaluation suite through
    LangSmith's evaluation framework.
    """

    print("=" * 60)
    print("Motor OD Claim Adjudicator")
    print("LangSmith LLM-as-a-Judge Evaluation")
    print("=" * 60)

    print(
        f"LangSmith project: {LANGSMITH_PROJECT}"
    )

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    if not LANGSMITH_API_KEY:
        raise RuntimeError(
            "LANGCHAIN_API_KEY is not configured."
        )

    # -----------------------------------------------------
    # Create LangSmith dataset
    # -----------------------------------------------------

    dataset_name = (
        "motor-od-claim-adjudicator-evaluation"
    )

    try:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=(
                "Evaluation dataset for Motor OD "
                "claim adjudication."
            ),
        )

        print(
            f"Created LangSmith dataset: "
            f"{dataset_name}"
        )

    except Exception:
        # Dataset may already exist.
        datasets = list(
            client.list_datasets(
                dataset_name=dataset_name
            )
        )

        if not datasets:
            raise

        dataset = datasets[0]

        print(
            f"Using existing LangSmith dataset: "
            f"{dataset_name}"
        )

    # -----------------------------------------------------
    # Add examples to dataset
    # -----------------------------------------------------

    existing_examples = list(
        client.list_examples(
            dataset_id=dataset.id
        )
    )

    existing_names = {
        example.metadata.get("case_name")
        for example in existing_examples
        if example.metadata
    }

    for case in EVALUATION_CASES:

        if case["name"] in existing_names:
            continue

        client.create_example(
            inputs=case["inputs"],
            outputs=case["reference"],
            dataset_id=dataset.id,
            metadata={
                "case_name": case["name"],
            },
        )

    # -----------------------------------------------------
    # Run LangSmith evaluation
    # -----------------------------------------------------

    print()
    print(
        "Running LangSmith evaluation..."
    )

    client.evaluate(
        target,
        data=dataset_name,
        evaluators=[
            decision_evaluator,
            llm_judge,
        ],
        experiment_prefix=LANGSMITH_PROJECT,
        description=(
            "Motor OD claim adjudication "
            "LLM-as-a-Judge evaluation."
        ),
        max_concurrency=1,
        blocking=True,
        upload_results=True,
    )

    # -----------------------------------------------------
    # Display Results
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("LangSmith Evaluation Completed")
    print("=" * 60)

    print(
        "Experiment results uploaded to LangSmith."
    )

    print(
        f"Project: {LANGSMITH_PROJECT}"
    )

    # -----------------------------------------------------
    # CI/CD Gate
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("Motor OD Evaluation Gate")
    print("=" * 60)

    # LangSmith ExperimentResults exposes results
    # through the returned object. We additionally
    # execute the deterministic checks locally so that
    # the CI/CD pipeline has a reliable exit status.

    local_results = []

    for case in EVALUATION_CASES:

        print()
        print(
            f"Evaluating case: {case['name']}"
        )

        try:

            result = run_claim(
                case["inputs"]
            )

            actual = str(
                result["decision"]
            ).upper()

            expected = str(
                case["reference"]["decision"]
            ).upper()

            passed = actual == expected

            local_results.append(
                passed
            )

            print(
                f"Expected decision: {expected}"
            )

            print(
                f"Actual decision:   {actual}"
            )

            print(
                f"Result: {'PASS' if passed else 'FAIL'}"
            )

        except RuntimeError as exc:

            print(
                f"Evaluation error: {exc}"
            )

            local_results.append(False)

    passed_count = sum(local_results)
    total_count = len(local_results)

    print()
    print("=" * 60)
    print("Evaluation Summary")
    print("=" * 60)

    print(
        f"Passed: {passed_count}/{total_count}"
    )

    print(
        f"Failed: "
        f"{total_count - passed_count}/"
        f"{total_count}"
    )

    if total_count:
        pass_rate = (
            passed_count / total_count
        ) * 100
    else:
        pass_rate = 0

    print(
        f"Pass rate: {pass_rate:.1f}%"
    )

    print("=" * 60)

    if passed_count != total_count:

        raise SystemExit(
            "Motor OD LangSmith evaluation gate FAILED."
        )

    print(
        "Motor OD LangSmith evaluation gate PASSED."
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    run_evaluation()