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


# ============================================================
# Structured response schema
# ============================================================

class AIResponse(BaseModel):
    summary: str = Field(
        description="A short summary of the user's message"
    )

    sentiment: int = Field(
        description="Integer from 0 to 100. "
                    "0 = very negative, "
                    "50 = neutral, "
                    "100 = very positive"
    )

    response: str = Field(
        description="A helpful and natural answer to the user"
    )


# ============================================================
# JSON parser
# ============================================================

json_parser = JsonOutputParser(
    pydantic_object=AIResponse
)


# ============================================================
# Model factory
# ============================================================

def create_llm():

    if AI_PROVIDER == "openrouter":

        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not configured."
            )

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

    elif AI_PROVIDER == "huggingface":

        if not HF_TOKEN:
            raise ValueError(
                "HF_TOKEN is not configured."
            )

        return ChatOpenAI(
            model=HF_MODEL,
            api_key=HF_TOKEN,
            base_url="https://router.huggingface.co/v1",
            temperature=PARAMETERS["temperature"],
            max_tokens=PARAMETERS["max_output_tokens"],
        )

    else:
        raise ValueError(
            f"Unsupported AI provider: {AI_PROVIDER}"
        )


llm = create_llm()


# ============================================================
# RAG Prompt
# ============================================================

prompt = PromptTemplate(
    template="""
You are an intelligent AI assistant.

Your job is to answer the user's question using the
retrieved knowledge provided below.

RETRIEVED KNOWLEDGE
-------------------
{context}
-------------------

USER QUESTION
-------------------
{user_message}
-------------------

Instructions:

1. Use the retrieved knowledge when it is relevant.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information,
   clearly say that the available knowledge does not
   provide enough information.
4. Keep the answer natural and helpful.
5. Always return all required JSON fields.
6. Return ONLY valid JSON.

{format_instructions}
""",
    input_variables=[
        "context",
        "user_message",
        "format_instructions",
    ],
)


# ============================================================
# LCEL chain
# ============================================================

chain = (
    prompt
    | llm
    | json_parser
)


# ============================================================
# Generate response
# ============================================================

def generate_response(
    user_message: str,
    context: str = ""
) -> dict:

    result = chain.invoke({
        "user_message": user_message,
        "context": context,
        "format_instructions":
            json_parser.get_format_instructions(),
    })

    return result