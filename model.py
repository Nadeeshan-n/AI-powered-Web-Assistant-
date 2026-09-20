from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
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

from pydantic import BaseModel, Field


class AIResponse(BaseModel):

    summary: str = Field(
        default="",
        description="A short summary of the user's message"
    )

    sentiment: int = Field(
        default=50,
        description=(
            "Integer from 0 to 100. "
            "0 = very negative, "
            "50 = neutral, "
            "100 = very positive"
        )
    )

    response: str = Field(
        default="",
        description="A helpful and natural answer to the user"
    )

# ============================================================
# JSON parser
# ============================================================




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
structured_llm = llm.with_structured_output(
    AIResponse,
    method="function_calling"
)


# ============================================================
# RAG Prompt
# ============================================================

prompt = PromptTemplate(
    template="""
You are an intelligent AI assistant.

Use the retrieved knowledge below to answer the user's question.

RETRIEVED KNOWLEDGE
-------------------
{context}
-------------------

USER QUESTION
-------------------
{user_message}
-------------------

Rules:

- Use the retrieved knowledge when it is relevant.
- Do not invent information that is not supported by the retrieved knowledge.
- If the retrieved knowledge does not contain enough information,
  clearly say that the available knowledge does not provide enough information.
- Keep the answer natural and helpful.
""",
    input_variables=[
        "context",
        "user_message",
    ],
)


# ============================================================
# LCEL chain
# ============================================================

chain = prompt | structured_llm


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
    })

    if isinstance(result, AIResponse):
        return result.model_dump()

    return result

def generate_response(
    user_message: str,
    context: str = ""
) -> dict:

    result = chain.invoke({
        "user_message": user_message,
        "context": context,
    })

    if isinstance(result, AIResponse):

        data = result.model_dump()

    elif isinstance(result, dict):

        data = result

    else:

        raise ValueError(
            "Model returned an unsupported response type."
        )

    # Ensure required application fields exist
    data.setdefault(
        "summary",
        user_message[:100]
    )

    data.setdefault(
        "sentiment",
        50
    )

    data.setdefault(
        "response",
        "I could not generate a response."
    )

    return data