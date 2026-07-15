from utils.knowledge_loader import load_document
from utils.llm import generate_response


def technical_agent(message):
    context = load_document("UserManual.txt")
    return generate_response(message, context)
