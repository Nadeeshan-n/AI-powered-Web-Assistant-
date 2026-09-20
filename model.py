from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config import (
    AI_PROVIDER,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    HF_TOKEN,
    HF_MODEL,
    PARAMETERS,
)


class AIResponse(BaseModel):
    summary: str = Field(
        description="A short summary of the user's message"
    )

    sentiment: int = Field(
        description="Integer from 0 to 100"
    )

    response: str = Field(
        description="Helpful response to the user"
    )


json_parser = JsonOutputParser(
    pydantic_object=AIResponse
)


def create_llm():
    if AI_PROVIDER == "openrouter":
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not configured.")

        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=PARAMETERS["temperature"],
            max_tokens=PARAMETERS["max_output_tokens"],
            default_headers={
                "HTTP-Referer": "http://localhost:5000",
                "X-OpenRouter-Title": "AI-Powered Web Assistant",
            },
        )

    if AI_PROVIDER == "huggingface":
        if not HF_TOKEN:
            raise ValueError("HF_TOKEN is not configured.")

        return ChatOpenAI(
            model=HF_MODEL,
            api_key=HF_TOKEN,
            base_url="https://router.huggingface.co/v1",
            temperature=PARAMETERS["temperature"],
            max_tokens=PARAMETERS["max_output_tokens"],
        )

    raise ValueError(
        f"Unsupported AI provider: {AI_PROVIDER}"
    )


llm = create_llm()


prompt = PromptTemplate(
    template="""
You are an intelligent AI assistant.

Use the retrieved context to answer the user's question.

Retrieved context:
{context}

User message:
{user_message}

Rules:
- Use the retrieved context when it is relevant.
- Do not invent facts that are not supported by the context.
- If the context does not contain enough information, clearly say that you do not have enough information.
- Return only valid JSON.

{format_instructions}
""",
    input_variables=[
        "user_message",
        "context",
        "format_instructions",]
)


chain = prompt | llm | json_parser


def generate_response(
    user_message: str,
    context: str = ""
) -> dict:

    return chain.invoke({
        "user_message": user_message,
        "context": context,
        "format_instructions": json_parser.get_format_instructions(),
    })