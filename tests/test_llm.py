from app.agent.adjudicator import get_llm


llm = get_llm()

response = llm.invoke(
    "Reply with exactly: LLM connection successful"
)

print(response.content)