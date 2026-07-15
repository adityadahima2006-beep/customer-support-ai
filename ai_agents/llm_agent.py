import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(user_message, context):
    """
    Generate AI response using Gemini.
    """

    prompt = f"""
You are an intelligent Customer Support AI Assistant.

Answer the user's question ONLY using the provided context.

--------------------------------------------------
CONTEXT
--------------------------------------------------
{context}

--------------------------------------------------
CUSTOMER QUESTION
--------------------------------------------------
{user_message}

Rules:
1. Be polite.
2. Be professional.
3. Give step-by-step guidance if needed.
4. Don't invent information.
5. If the answer isn't available, politely recommend escalating to a human support agent.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"⚠ Gemini Error:\n\n{str(e)}"
