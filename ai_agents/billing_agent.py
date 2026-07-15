from utils.knowledge_loader import load_document
from utils.llm import generate_response


def billing_agent(message):

    context = (
        load_document("RefundPolicy.txt")
        + "\n\n"
        + load_document("Pricing.txt")
    )

    return generate_response(message, context)
