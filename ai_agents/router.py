from ai_agents.billing_agent import billing_agent
from ai_agents.technical_agent import technical_agent
from ai_agents.product_agent import product_agent
from ai_agents.complaint_agent import complaint_agent
from ai_agents.faq_agent import faq_agent
from ai_agents.handoff_agent import should_escalate, escalation_response


def route_query(intents, message):
    """
    Routes the customer query to the correct support agent.
    If the customer requests a human or the issue seems unresolved,
    the conversation is handed off immediately.
    """

    # Human Handoff / Escalation
    if should_escalate(message):
        return escalation_response()

    responses = []

    for intent in intents:

        if intent == "Billing":
            responses.append(billing_agent(message))

        elif intent == "Technical Support":
            responses.append(technical_agent(message))

        elif intent == "Product":
            responses.append(product_agent(message))

        elif intent == "Complaint":
            responses.append(complaint_agent(message))

        else:
            responses.append(faq_agent(message))

    if not responses:
        responses.append(
            "I'm sorry, I couldn't identify your request. Could you please provide more details?"
        )

    return "\n\n-----------------------------\n\n".join(responses)
