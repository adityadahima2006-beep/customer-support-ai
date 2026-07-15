import streamlit as st


def initialize_memory():
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = []


def add_message(role, message):
    st.session_state.conversation_memory.append(
        {
            "role": role,
            "message": message
        }
    )


def get_memory():
    return st.session_state.conversation_memory


def clear_memory():
    st.session_state.conversation_memory = []