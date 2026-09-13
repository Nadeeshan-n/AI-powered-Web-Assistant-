from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL_ID,
    PARAMETERS
)


class AIResponse(BaseModel):
    summary: str = Field(
        description="A short summary of the user's message"
    )

    sentiment: int = Field(
        description="Sentiment score from 0 (very negative) to 100 (very positive)"
    )

    response: str = Field(
        description="A helpful response to the user's message"
    )


json_parser = JsonOutputParser(
    pydantic_object=AIResponse
)


gemini_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL_ID,
    google_api_key=GEMINI_API_KEY,
    temperature=PARAMETERS["temperature"],
    max_output_tokens=PARAMETERS["max_output_tokens"]
)


gemini_template = PromptTemplate(
    template="""You are an AI assistant on experimental state.

{system_prompt}

You must analyze the user's message and return a JSON object.

The JSON MUST contain exactly these three fields:

1. "summary"
   A short summary of what the user said.

2. "sentiment"
   An integer between 0 and 100.
   0 = very negative
   50 = neutral
   100 = very positive

3. "response"
   A helpful and natural response to the user.

{format_prompt}

User message:
{user_prompt}

IMPORTANT:
- Always provide all three fields.
- Never omit a field.
- Never return an empty JSON object.
- Return ONLY valid JSON.
""",
    input_variables=[
        "system_prompt",
        "user_prompt",
        "format_prompt"
    ]
)


def gemini_response(system_prompt, user_prompt):

    chain = gemini_template | gemini_llm | json_parser

    result = chain.invoke({
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "format_prompt": json_parser.get_format_instructions()
    })

    return result