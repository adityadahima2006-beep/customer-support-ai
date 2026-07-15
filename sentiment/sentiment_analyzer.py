from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze the sentiment of the user's message.
    Returns:
        Positive
        Neutral
        Negative
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Positive"

    elif polarity < -0.2:
        return "Negative"

    else:
        return "Neutral"