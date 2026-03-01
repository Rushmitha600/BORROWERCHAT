# Borrower Chatbot - AI Assistant

A comprehensive borrower assistance chatbot with EMI calculator, eligibility checker, and AI-powered suggestions, inspired by Infosys Springboard.

## Features

- 🤖 **AI Assistant Sidebar**: Contextual help and suggested questions
- 💬 **Interactive Chatbot**: Natural language conversation with greeting responses
- 🌓 **Dark/Light Mode**: Toggle between themes with persistent storage
- 📊 **EMI Calculator**: Calculate monthly installments with multiple loan options
- 📈 **Eligibility Checker**: Color-coded results based on credit score
  - 🔴 Below 600: Not eligible
  - 🟡 600-799: Moderate eligibility
  - 🟢 800+: Eligible
- 💰 **Missed Payment Calculator**: Calculate penalties for missed payments
- 🎯 **Multiple Loan Types**: Personal, Home, Car, Education loans
- 💾 **Conversation Logging**: Store chat history for analysis

## Technology Stack

### Backend
- Python Flask
- RESTful API architecture
- NLTK for basic NLP
- JSON file-based database

### Frontend
- HTML5
- CSS3 with animations
- Vanilla JavaScript (ES6+)
- Font Awesome Icons
- Responsive design

## Project Structure
borrower-chatbot/
│
├── backend/
│ ├── app.py # Main Flask application
│ ├── chatbot.py # Chatbot logic
│ ├── emi_calculator.py # EMI calculation logic
│ ├── eligibility_checker.py # Credit score checking
│ ├── faq_data.py # FAQ management
│ ├── utils.py # Utility functions
│ └── requirements.txt # Python dependencies
│
├── frontend/
│ ├── index.html # Main HTML file
│ ├── style.css # Styles and themes
│ ├── script.js # Frontend logic
│ └── assets/ # Images and icons
│
├── database/
│ ├── faq_database.json # FAQ storage
│ ├── loan_products.json # Loan product data
│ └── conversation_logs.json # Chat history
│
├── config.py # Configuration settings
└── README.md # Documentation