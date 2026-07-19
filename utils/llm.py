import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


def generate_response(user_message, context):

    if client is None:
        return (
            "⚠ Gemini API is not configured.\n\n"
            "Please check your GEMINI_API_KEY."
        )

    prompt = f"""
You are an intelligent Customer Support AI Assistant.

Answer the user's question ONLY using the provided context.

CONTEXT:
{context}

CUSTOMER QUESTION:
{user_message}

Rules:
1. Be polite.
2. Be professional.
3. Give step-by-step guidance if needed.
4. Don't invent information.
5. If the answer isn't available, recommend escalating to a human support agent.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and hasattr(response, "text"):
            return response.text

        return "⚠ Gemini generated an empty response."

    except Exception as e:

        return f"⚠ Gemini Error:\n\n{str(e)}"
