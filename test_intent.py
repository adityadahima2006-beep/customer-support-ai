from services.intent_service import predict_intent

query = "My debit card has not arrived."

intent = predict_intent(query)

print("Predicted Intent:", intent)
