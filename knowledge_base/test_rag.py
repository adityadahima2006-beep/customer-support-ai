from knowledge_base.vector_store import search

question = input("Ask a question: ")

results = search(question)

print("\nBest Match\n")

for r in results:
    print("File:", r["file"])
    print()
    print(r["content"])