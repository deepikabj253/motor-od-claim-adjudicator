# 🚗 Motor OD Claim Adjudicator

AI-powered Motor Own Damage (OD) Insurance Claim Adjudication system.

The application evaluates motor insurance claims against the applicable policy, retrieves relevant policy information, considers previous vehicle claim history, performs deterministic loss assessment, and generates an explainable adjudication decision.

---

## Features

- Motor Own Damage claim intake
- FastAPI backend
- Streamlit user interface
- LangGraph-based claim adjudication workflow
- PII detection and anonymization using Microsoft Presidio
- Policy retrieval using RAG
- ChromaDB vector store
- Mem0-based vehicle claim memory
- Vehicle-specific claim history
- Deterministic IMT loss assessment
- LLM-based claim adjudication
- Explainable decisions
- LangSmith tracing and observability
- Support for:
  - `APPROVE`
  - `REJECT`
  - `NEEDS_REVIEW`

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Agent Workflow | LangGraph |
| LLM | OpenAI |
| RAG | LangChain + ChromaDB |
| PII Protection | Microsoft Presidio |
| Memory | Mem0 |
| Observability | LangSmith |
| Validation | Pydantic |
| Language | Python |

---

## Project Structure

```text
motor-od-claim-adjudicator/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── prompt.py
│   │   ├── adjudicator.py
│   │   └── preprocessor.py
│   │
│   ├── memory/
│   │   └── memory.py
│   │
│   ├── pii/
│   │   └── recognizer.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   │
│   ├── schemas/
│   │   └── claim.py
│   │
│   ├── tools/
│   │   └── imt_calculator.py
│   │
│   ├── main.py
│   └── streamlit_app.py
│
├── data/
│   └── policies/
│       └── motor_policy.txt
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
````

---

## Claim Processing Workflow

The claim goes through the following stages:

1. Claim is submitted through Streamlit.
2. Streamlit sends the claim to FastAPI.
3. FastAPI validates the request using Pydantic.
4. LangGraph starts the adjudication workflow.
5. Sensitive information is detected and anonymized using Presidio.
6. A deterministic vehicle memory ID is generated.
7. Mem0 retrieves previous claim history for the vehicle.
8. Relevant policy information is retrieved using RAG.
9. The IMT calculator performs deterministic loss assessment.
10. The LLM evaluates the claim using the claim details, policy evidence, claim history, and assessment.
11. The system generates:

    * `APPROVE`
    * `REJECT`
    * `NEEDS_REVIEW`
12. The adjudicated claim is stored in Mem0 for future reference.
13. LangSmith provides tracing and observability.

---

## PII Protection

The application uses Microsoft Presidio to identify and anonymize sensitive information.

For example:

```text
Original:

TN01AB1234

Masked:

<INDIAN_RC>
```

The original vehicle number is not used directly as the Mem0 user identifier.

Instead, a deterministic anonymized vehicle ID is generated.

Example:

```text
vehicle_4fc9fcd3fbfbc8f2
```

This allows the application to retrieve vehicle-specific history without exposing the original registration number.

---

## Vehicle Memory

Mem0 is used to maintain historical claim information.

Example stored information:

```text
Previous rear bumper damage claim around December 2025.

No Claims Bonus declared during renewal was 35%.
```

When another claim is submitted for the same vehicle, the system retrieves relevant historical information.

A different vehicle receives a different memory ID and therefore does not receive the previous vehicle's history.

---

## Policy RAG

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant policy information.

The policy contains information about:

* Accidental damage
* Fire and explosion
* Theft
* Natural calamities
* Policy exclusions
* Driving licence requirements
* Vehicle usage
* Deductibles
* Claim assessment

The retrieved policy context is provided to the adjudication agent before making the decision.

---

## IMT Loss Assessment

The application performs deterministic claim assessment using the IMT calculator.

The assessment considers:

* Damaged part
* Part category
* Claimed amount
* Depreciation
* Applicable deductible
* Approved amount
* Net payable amount

The financial calculation is performed deterministically rather than relying on the LLM for arithmetic.

---

## Adjudication

The LLM evaluates the claim using:

* Claim details
* Accident description
* Licence status
* Vehicle and policy details
* Retrieved policy evidence
* Previous vehicle claim history
* IMT assessment

The final response contains:

```text
Decision
Reason
Policy Evidence
Missing Information
```

Possible decisions:

```text
APPROVE
REJECT
NEEDS_REVIEW
```

---

## LangSmith Observability

LangSmith is configured for tracing and observability of the LangGraph workflow.

This allows inspection of:

* Agent execution
* LLM calls
* Retrieval steps
* Inputs and outputs
* Execution traces
* Errors
* Latency

The LangSmith project can be configured using environment variables.

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=motor-od-claim-adjudicator
```

Do not commit `.env` or API keys to Git.

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Backend

Start FastAPI:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "Motor OD Claim Adjudicator"
}
```

---

## Running Streamlit

In another terminal:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit application provides:

* Claim scenario selection
* Customer details
* Vehicle details
* Policy details
* Accident details
* Garage estimate
* Claim preview
* Previous claim history
* IMT assessment
* Adjudication result

---

## API Endpoint

### POST

```text
/api/v1/claims/adjudicate
```

Example request:

```json
{
  "customer_name": "Demo Customer",
  "vehicle_number": "TN01AB1234",
  "dl_number": "DL123456789",
  "vin": "TESTVIN123",
  "accident_description": "The vehicle hit a road divider and the front bumper was damaged.",
  "accident_type": "Impact with Object",
  "licence_status": "Valid",
  "vehicle_age": "2 - 5 Years",
  "engine_cc": "Up to 1500cc",
  "policy_type": "Motor Own Damage",
  "vehicle_usage": "Private",
  "zero_dep": "No",
  "engine_protect": "No",
  "consumables_cover": "No",
  "claim_amount": 4500,
  "garage_estimate": [
    {
      "part_name": "Front Bumper",
      "category": "PLASTIC",
      "claimed_amount": 4500
    }
  ]
}
```

---

## Example Decision

For an accidental damage claim:

```text
Decision:
APPROVE

Reason:
The reported incident is covered under the policy's
accidental damage provision and no applicable exclusion
is triggered.

Policy Evidence:
The policy covers damage to the insured vehicle caused
by accidents, including collision and impact with an object.

Missing Information:
NONE
```

---

## Example Claim History

For a vehicle with previous claim history:

```text
Previous rear bumper damage claim around December 2025.

No Claims Bonus declared during renewal was 35%.
```

The history is retrieved using the vehicle-specific Mem0 memory ID.

---

## Testing

The project previously contained unit tests during development.

The current application can be validated using:

```bash
python -c "from app.agent.prompt import build_adjudication_prompt; print('Prompt loaded successfully')"
```

```bash
python -c "from app.agent.graph import build_claim_graph; print('Graph loaded successfully')"
```

```bash
python -c "from app.memory.memory import get_memory; print('Mem0 memory initialized successfully')"
```

---

## Security

The following files and generated data should not be committed:

```text
.env
venv/
data/chroma/
data/memory/
__pycache__/
.pytest_cache/
```

API keys and other secrets must be stored in `.env`.

---

## Project Status

The application currently supports:

* FastAPI claim API
* Streamlit claim UI
* PII anonymization
* Policy RAG
* LangGraph orchestration
* Mem0 vehicle memory
* Historical claim retrieval
* IMT claim assessment
* LLM adjudication
* LangSmith observability