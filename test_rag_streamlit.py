import streamlit as st
from knowledge_base.vector_store import search

st.set_page_config(page_title="RAG Knowledge Base Test", page_icon="🤖")

st.title("🤖 Customer Support RAG Test")

st.write("Ask any question related to the company's knowledge base.")

question = st.text_input("Enter your question:")

if st.button("Search"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        results = search(question)

        st.success("Best Match Found!")

        for result in results:
            st.subheader(f"📄 {result['file']}")
            st.write(result["content"])