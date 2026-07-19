from ai_agents.billing_agent import billing_agent
from ai_agents.technical_agent import technical_agent
from ai_agents.product_agent import product_agent
from ai_agents.complaint_agent import complaint_agent
from ai_agents.faq_agent import faq_agent
from ai_agents.handoff_agent import (
    should_escalate,
    escalation_response
)


def route_query(intents, message):
    """
    Route the customer query to the appropriate support agent.
    """

    # -------------------------
    # Human Escalation
    # -------------------------
    if should_escalate(message):
        return escalation_response()

    # -------------------------
    # Handle Empty Intent List
    # -------------------------
    if not intents:
        return faq_agent(message)

    responses = []

    for intent in intents:

        try:

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

        except Exception as e:

            responses.append(
                f"⚠ Error while processing '{intent}' agent:\n{str(e)}"
            )

    if not responses:

        responses.append(
            "I'm sorry, I couldn't understand your request. Could you please provide more details?"
        )

    return "\n\n-----------------------------\n\n".join(responses)
