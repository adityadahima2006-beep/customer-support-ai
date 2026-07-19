# agent/intent_agent.py

def detect_intent(message):

    message = message.lower()

    billing_keywords = [
        "bill", "billing", "payment", "refund", "invoice",
        "price", "charge", "money", "subscription", "plan"
    ]

    technical_keywords = [
        "error", "issue", "bug", "login", "password",
        "otp", "failed", "problem", "technical",
        "not working", "crash"
    ]

    complaint_keywords = [
        "complaint", "bad", "poor", "worst",
        "angry", "cancel", "lost", "stolen"
    ]

    product_keywords = [
        "product", "feature", "service",
        "details", "information"
    ]

    for word in billing_keywords:
        if word in message:
            return ["Billing"]

    for word in technical_keywords:
        if word in message:
            return ["Technical Support"]

    for word in complaint_keywords:
        if word in message:
            return ["Complaint"]

    for word in product_keywords:
        if word in message:
            return ["Product"]

    return ["FAQ"]
