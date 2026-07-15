from utils.knowledge_loader import load_document
from utils.llm import generate_response


def complaint_agent(message):

    context = (
        load_document("RefundPolicy.txt")
        + "\n\n"
        + load_document("Warranty.txt")
    )

    return generate_response(message, context)
