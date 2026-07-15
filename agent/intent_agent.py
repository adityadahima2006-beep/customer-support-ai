from sentence_transformers import SentenceTransformer, util

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Banking77 intents
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
    "transfer_not_received",
    "card_payment_not_recognised",
    "declined_card_payment",
    "cash_withdrawal_charge",
    "exchange_rate"
]

# Create embeddings
intent_embeddings = model.encode(
    intent_labels,
    convert_to_tensor=True
)


def detect_intent(message):

    query_embedding = model.encode(
        message,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        query_embedding,
        intent_embeddings
    )

    index = similarity.argmax().item()

    banking_intent = intent_labels[index]

    # Map Banking77 intents to your AI agents
    if banking_intent in [
        "activate_my_card",
        "card_arrival",
        "change_pin",
        "cash_withdrawal",
        "cash_withdrawal_charge",
        "exchange_rate"
    ]:
        return ["Billing"]

    elif banking_intent in [
        "top_up_failed",
        "beneficiary_not_allowed",
        "transfer_not_received",
        "card_payment_not_recognised",
        "declined_card_payment"
    ]:
        return ["Technical Support"]

    elif banking_intent in [
        "lost_or_stolen_card"
    ]:
        return ["Complaint"]

    elif banking_intent in [
        "request_refund"
    ]:
        return ["Billing"]

    elif banking_intent in [
        "verify_identity"
    ]:
        return ["Technical Support"]

    else:
        return ["FAQ"]
