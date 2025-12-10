from flask import Flask, render_template, request, jsonify
from llm import LegalChatbot
import os

app = Flask(__name__)

chatbot = LegalChatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    response = chatbot.answer_query(user_message)
    
    return jsonify({"answer": response})

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(chatbot.get_history())

@app.route("/clear", methods=["POST"])
def clear_history():
    chatbot.clear_history()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)