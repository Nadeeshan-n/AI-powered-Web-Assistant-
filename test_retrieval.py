from services.rag_service import rag_service


question = "What is the purpose of this document?"

documents = rag_service.retrieve(
    question,
    k=4
)

for i, document in enumerate(documents, start=1):

    print("\n" + "=" * 60)
    print(f"RESULT {i}")
    print("=" * 60)

    print(
        document.page_content[:1000]
    )

    print(
        "\nMetadata:",
        document.metadata
    )