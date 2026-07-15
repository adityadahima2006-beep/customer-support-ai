from sentiment.sentiment_analyzer import analyze_sentiment

while True:
    text = input("Enter message: ")

    if text.lower() == "exit":
        break

    print("Sentiment:", analyze_sentiment(text))
    print()