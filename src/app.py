from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import difflib
import sys

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

# ==============================
# 📌 Loan Products Data
# ==============================

loan_products = {
    'car': {'name': 'Car Loan', 'rate': 9.5},
    'education': {'name': 'Education Loan', 'rate': 11.0},
    'home': {'name': 'Home Loan', 'rate': 8.5},
    'personal': {'name': 'Personal Loan', 'rate': 10.5}
}

@app.route('/api/loan-products', methods=['GET'])
def get_loan_products():
    return jsonify(loan_products)


# ==============================
# 📌 EMI Calculator API
# ==============================

@app.route('/api/calculate-emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        rate = float(data.get('rate', 0))
        tenure = int(data.get('tenure', 0))

        if amount <= 0 or rate <= 0 or tenure <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        monthly_rate = rate / (12 * 100)

        emi = amount * monthly_rate * (1 + monthly_rate)**tenure / \
              ((1 + monthly_rate)**tenure - 1)

        total_payment = emi * tenure
        total_interest = total_payment - amount

        return jsonify({
            'emi': round(emi, 2),
            'total_interest': round(total_interest, 2),
            'total_payment': round(total_payment, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==============================
# 📌 FAQ Chatbot Integration
# ==============================

from chatbot import ChatBot

chatbot = ChatBot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = chatbot.get_response(user_message)

        return jsonify({
            "response": response,
            "suggestions": chatbot.get_suggestions(user_message)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# 📌 Serve Frontend
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ==============================
# 🚀 Run Server
# ==============================

if __name__ == '__main__':
    app.run(debug=True, port=5000)
