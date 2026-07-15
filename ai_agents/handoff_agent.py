import random

ESCALATION_KEYWORDS = [
    "human",
    "agent",
    "representative",
    "manager",
    "talk to human",
    "connect me to an agent",
    "customer support",
    "real person",
    "not resolved",
    "still not working",
    "didn't work",
    "did not work",
    "contacted you",
    "many times",
    "frustrated",
    "complaint",
    "escalate"
]


def should_escalate(message):
    message = message.lower()

    for keyword in ESCALATION_KEYWORDS:
        if keyword in message:
            return True

    return False


def generate_ticket():
    return f"CS-{random.randint(1000, 9999)}"


def escalation_response():
    ticket = generate_ticket()

    return f"""
I'm sorry that we couldn't resolve your issue.

Your request has been escalated to a human support agent.

Ticket ID: {ticket}

A support representative will contact you shortly.
"""
