from app.rag.ingest import create_vector_store


vector_store = create_vector_store()

print("Policy documents successfully added to ChromaDB.")

results = vector_store.similarity_search(
    "Is accidental vehicle damage covered?",
    k=2
)

print("\nRetrieved policy content:")

for result in results:
    print(result.page_content)
    print("Source:", result.metadata)