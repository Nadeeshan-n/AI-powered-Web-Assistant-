from model import generate_response
from services.rag_service import rag_service


def generate_ai_response(
    user_message: str
) -> dict:

    # --------------------------------------------------------
    # 1. Retrieve relevant documents
    # --------------------------------------------------------

    documents = rag_service.search(
        user_message,
        k=4
    )

    # --------------------------------------------------------
    # 2. Convert documents into context
    # --------------------------------------------------------

    context = rag_service.build_context(
        documents
    )

    # --------------------------------------------------------
    # 3. Send question + context to LLM
    # --------------------------------------------------------

    result = generate_response(
        user_message=user_message,
        context=context
    )

    # --------------------------------------------------------
    # 4. Attach source information
    # --------------------------------------------------------

    result["sources"] = (
        rag_service.get_sources(
            documents
        )
    )

    return result