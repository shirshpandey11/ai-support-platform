from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def classify_sentiment(text: str) -> str:

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "POSITIVE"

    elif polarity < 0:
        return "NEGATIVE"

    return "NEUTRAL"


def categorize_tickets(messages, n_clusters=5):
    vectorizer = TfidfVectorizer(stop_words='english')

    X = vectorizer.fit_transform(messages)

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )

    labels = kmeans.fit_predict(X)

    return labels.tolist()


def detect_category(message):

    text = message.lower()

    if "refund" in text:
        return "Refund"

    elif "delay" in text:
        return "Delivery Delay"
    elif "damaged" in text:
        return "Damaged Product"

    elif "payment" in text:
        return "Payment Issue"

    elif "login" in text:
        return "Login Problem"

    return "General"


def suggest_reply(text):

    text = text.lower()

    if "refund" in text:
        return (
            "We sincerely apologize for the inconvenience. "
            "Your refund request is being processed."
        )
    if "delay" in text:
        return (
            "We apologize for the delivery delay. "
            "Our logistics team is actively tracking your shipment."
        )

    if "damaged" in text:
        return (
            "We are sorry to hear that your product arrived damaged. "
            "We will arrange a replacement immediately."
        )

    return (
        "Thank you for contacting support. "
        "Our team is reviewing your issue and will respond shortly."
    )