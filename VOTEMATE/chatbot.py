import spacy
import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, request, jsonify
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

nltk.download("punkt")
patterns = [
    (r"hi|hello|hey", ["Hello! How can I assist you today?", "Hi there! What’s on your mind?"]),
    (r"how are you?", ["I'm good! Thanks for asking. How about you?", "I'm doing well! What about you?"]),
    (r"what is your name?", ["I am ChatAI, your virtual assistant!", "You can call me ChatAI."]),
    (r"bye|goodbye", ["Goodbye! Have a great day!", "See you later! Take care."]),
    (r"thank you|thanks", ["You're welcome! Glad I could help.", "No problem! Anytime."]),
    (r"what can you do?", ["I can chat with you, answer questions, and analyze text!", "I can help with cooking, daily tasks, and general advice!"]),
]

chatbot = Chat(patterns, reflections)

def process_input(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]

    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        sentiment_text = "That sounds positive! 😊"
    elif sentiment < 0:
        sentiment_text = "That sounds a bit negative. 😟 I'm here to help!"
    else:
        sentiment_text = "That sounds neutral. 🤔"

    return {
        "entities": entities,
        "verbs": verbs,
        "nouns": nouns,
        "sentiment": sentiment_text
    }

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot.respond(user_input)

    if not response:
        processed = process_input(user_input)
        response = processed["sentiment"]
        
        if processed["entities"]:
            response += f" Also, I see you're talking about {', '.join(processed['entities'])}. Tell me more!"
        elif processed["verbs"]:
            response += f" I noticed you mentioned the actions: {', '.join(processed['verbs'])}. What are you up to?"
        elif processed["nouns"]:
            response += f" I see some interesting words: {', '.join(processed['nouns'])}. What’s on your mind?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="192.168.229.98", port=5000, debug=True)