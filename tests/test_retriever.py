from app.rag.retriever import get_retriever


retriever = get_retriever()

query = "Is accidental vehicle damage covered by the policy?"

results = retriever.invoke(query)

print("Query:")
print(query)

print("\nRetrieved Policy Information:")

for result in results:
    print("\n---")
    print(result.page_content)
    print("Source:", result.metadata)