from model import generate_response
from services.rag_service import rag_service


def generate_ai_response(user_message: str) -> dict:
    """
    Generate an AI response using retrieved document context.
    """

    context = rag_service.build_context(
        user_message,
        k=4
    )

    return generate_response(
        user_message=user_message,
        context=context
    )