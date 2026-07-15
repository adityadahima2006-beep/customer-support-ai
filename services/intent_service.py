from sentence_transformers import SentenceTransformer, util

# Load AI model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Banking intents (Demo Version)
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

# Create embeddings for all intents
intent_embeddings = model.encode(
    intent_labels,
    convert_to_tensor=True
)

def predict_intent(user_query):
    """
    Predict the intent of the customer query.
    """

    query_embedding = model.encode(
        user_query,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        query_embedding,
        intent_embeddings
    )

    predicted_index = similarity.argmax().item()

    return intent_labels[predicted_index]