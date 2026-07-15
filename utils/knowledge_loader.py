import os


def load_document(filename):

    path = os.path.join("knowledge_base", filename)

    if not os.path.exists(path):
        return "Document not found."

    with open(path, "r", encoding="utf-8") as file:
        return file.read()