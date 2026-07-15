from utils.knowledge_loader import load_document
from utils.llm import generate_response


def product_agent(message):

    context = (
        load_document("Warranty.txt")
        + "\n\n"
        + load_document("Pricing.txt")
        + "\n\n"
        + load_document("ShippingPolicy.txt")
    )

    return generate_response(message, context)
