"""

Example code for loading guide/ipv_response_guide.md as a system instruction
across Anthropic, OpenAI, and Google Gemini APIs.

Before running:
    pip install anthropic openai google-genai

Set API keys as environment variables:
    export ANTHROPIC_API_KEY="..."
    export OPENAI_API_KEY="..."
    export GEMINI_API_KEY="..."

Do not put API keys directly in this file.
"""

from pathlib import Path


GUIDE_PATH = Path("guide/ipv_response_guide.md")


def load_guide() -> str:
    """Load the IPV response guide as a system prompt."""
    return GUIDE_PATH.read_text(encoding="utf-8")


# -------------------------
# Anthropic / Claude
# -------------------------

def call_anthropic(user_msg: str) -> str:
    """
    Sends a user message to Claude with the IPV response guide
    loaded as the system prompt.
    """
    from anthropic import Anthropic

    system_prompt = load_guide()
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_msg}
        ],
    )

    return response.content[0].text


# -------------------------
# OpenAI
# -------------------------

def call_openai(user_msg: str) -> str:
    """
    Sends a user message to OpenAI with the IPV response guide
    loaded as the model instructions.
    """
    from openai import OpenAI

    system_prompt = load_guide()
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o",
        instructions=system_prompt,
        input=user_msg,
    )

    return response.output_text


# -------------------------
# Google Gemini
# -------------------------

def call_gemini(user_msg: str) -> str:
    """
    Sends a user message to Gemini with the IPV response guide
    loaded as the system instruction.
    """
    from google import genai
    from google.genai import types

    system_prompt = load_guide()
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=user_msg,
    )

    return response.text


# -------------------------
# Demo
# -------------------------

if __name__ == "__main__":
    user_msg = (
        "My partner checks my phone and gets angry when I see my friends. "
        "I don't know if I'm overreacting."
    )

    print("\n--- OpenAI example ---")
    print(call_openai(user_msg))

    # Uncomment these if you have the corresponding API keys installed.
    #
    # print("\n--- Anthropic example ---")
    # print(call_anthropic(user_msg))
    #
    # print("\n--- Gemini example ---")
    # print(call_gemini(user_msg))
