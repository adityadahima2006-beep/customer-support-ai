import streamlit as st

from database.db import save_chat
from agent.intent_agent import detect_intent
from ai_agents.router import route_query
from ai_agents.llm_agent import generate_response
from knowledge_base.vector_store import search

from memory.conversation_memory import (
    initialize_memory,
    add_message
)

from sentiment.sentiment_analyzer import analyze_sentiment


# Greeting words
GREETINGS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
]


def show_chat():

    st.subheader("💬 Customer Support Chat")

    initialize_memory()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:

        sentiment = analyze_sentiment(user_input)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        add_message("user", user_input)

        with st.chat_message("user"):
            st.write(user_input)

        # Greeting
        if user_input.lower().strip() in GREETINGS:

            ai_response = (
                "👋 Hello!\n\n"
                "Welcome to Customer Support AI.\n"
                "How can I help you today?"
            )

        else:

            # ------------------------
            # Detect Intent
            # ------------------------
            intents = detect_intent(user_input)

            # ------------------------
            # Route Query
            # ------------------------
            agent_response = route_query(
                intents,
                user_input
            )

            # ------------------------
            # Knowledge Base Search
            # ------------------------
            try:

                results = search(user_input)

                if results:
                    kb_context = results[0]["content"]
                else:
                    kb_context = "No relevant information found in the knowledge base."

            except Exception as e:

                st.error(f"Knowledge Base Error:\n{e}")

                kb_context = "Knowledge base unavailable."

            # ------------------------
            # Build Context
            # ------------------------
            context = f"""
Agent Response:
{agent_response}

Knowledge Base:
{kb_context}
"""

            # ------------------------
            # Gemini Response
            # ------------------------
            with st.spinner("🤖 Generating response..."):

                try:

                    ai_response = generate_response(
                        user_input,
                        context
                    )

                except Exception as e:

                    st.error(f"Gemini Error:\n{e}")

                    ai_response = (
                        f"{agent_response}\n\n"
                        f"Gemini Error:\n{str(e)}"
                    )

        # ------------------------
        # Sentiment Handling
        # ------------------------
        if sentiment == "Negative":

            ai_response = (
                "😔 I'm sorry to hear that.\n\n"
                + ai_response
            )

        elif sentiment == "Positive":

            ai_response = (
                "😊 Thank you for your positive feedback!\n\n"
                + ai_response
            )

        # ------------------------
        # Save Assistant Message
        # ------------------------
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        add_message("assistant", ai_response)

        # ------------------------
        # Save Chat History
        # ------------------------
        save_chat(
            st.session_state.get("username", "Guest"),
            user_input,
            ai_response
        )

        # ------------------------
        # Display Assistant Response
        # ------------------------
        with st.chat_message("assistant"):
            st.write(ai_response)
