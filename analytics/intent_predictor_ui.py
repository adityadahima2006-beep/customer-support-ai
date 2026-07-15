import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="Banking Intent Detector")

st.title("🏦 Banking Intent Detector")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

with st.spinner("Loading AI model..."):
    model = load_model()

st.success("✅ AI Model Ready")

intent_labels = [
    "activate_my_card",
    "card_arrival",
    "change_pin",
    "cash_withdrawal",
    "lost_or_stolen_card",
    "request_refund",
    "verify_identity",
    "top_up_failed",
    "beneficiary_not_allowed",
    "transfer_not_received"
]

intent_embeddings = model.encode(
    intent_labels,
    convert_to_tensor=True
)

query = st.text_input("Customer Query")

if st.button("Predict Intent"):
    if query.strip():
        query_embedding = model.encode(
            query,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            query_embedding,
            intent_embeddings
        )

        index = similarity.argmax().item()

        st.success(f"Predicted Intent: {intent_labels[index]}")
