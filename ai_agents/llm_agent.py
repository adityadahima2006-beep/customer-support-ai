import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


def generate_response(user_message, context):
    """
    Generate AI response using Google Gemini.
    """

    # -------------------------------
    # API Key Check
    # -------------------------------
    if client is None:
        return (
            "⚠ Gemini API is not configured.\n\n"
            "Please check your GEMINI_API_KEY in the .env file."
        )

    # -------------------------------
    # Prompt
    # -------------------------------
    prompt = f"""
You are an intelligent Customer Support AI Assistant.

Your job is to answer ONLY from the provided context.

--------------------------------------------------
CONTEXT
--------------------------------------------------
{context}

--------------------------------------------------
CUSTOMER QUESTION
--------------------------------------------------
{user_message}

Instructions:
- Be polite.
- Be professional.
- Give clear step-by-step guidance.
- Never invent information.
- If the answer is unavailable in the context, politely recommend contacting a human support agent.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response is None:
            return "⚠ Gemini returned an empty response."

        if hasattr(response, "text") and response.text:
            return response.text

        return "⚠ Gemini generated no text."

    except Exception as e:

        return (
            "⚠ Gemini API Error\n\n"
            f"{str(e)}"
        )
