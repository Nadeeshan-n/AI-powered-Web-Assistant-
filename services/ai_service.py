from model import generate_response


def generate_ai_response(user_message: str) -> dict:
    return generate_response(user_message)