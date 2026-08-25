Build an AI-powered Motor Own Damage (OD) claim adjudication system that evaluates insurance claims against the applicable policy and provides an explainable decision.
The system should:
Accept claim details.
Protect sensitive information using PII masking.
Retrieve relevant policy information using RAG.
Use an LLM to evaluate the claim.
Generate `APPROVE`, `REJECT`, or `NEEDS_REVIEW`.
Expose the application through FastAPI.
Provide a user interface using Streamlit.
Add LangSmith for tracing and observability.