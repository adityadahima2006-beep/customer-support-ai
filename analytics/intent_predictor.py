from sentence_transformers import SentenceTransformer, util

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Banking intents
intent_labels = [
    "activate_my_card",
    "card_arrival",
    "change_pin",
    "cash_withdrawal",
    "lost_or_stolen_card",
    "beneficiary_not_allowed",
    "transfer_not_received",
    "top_up_failed",
    "request_refund",
    "verify_identity"
]

# Create embeddings for intents
intent_embeddings = model.encode(intent_labels, convert_to_tensor=True)


def predict_intent(user_query):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    similarity = util.cos_sim(query_embedding, intent_embeddings)

    index = similarity.argmax().item()

    return intent_labels[index]


# -------------------------
# Test
# -------------------------

while True:
    query = input("\nCustomer: ")

    if query.lower() == "exit":
        break

    intent = predict_intent(query)

    print("Predicted Intent:", intent)