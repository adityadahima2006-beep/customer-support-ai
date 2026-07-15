from utils.knowledge_loader import load_document
from utils.llm import generate_response


def faq_agent(message):

    context = load_document("FAQ.txt")

    return generate_response(message, context)
