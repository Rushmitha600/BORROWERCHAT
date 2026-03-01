import os

class Config:
    # Application settings
    APP_NAME = "Borrower Chatbot"
    VERSION = "1.0.0"
    DEBUG = True
    
    # Database settings
    DATABASE_PATH = "database/"
    FAQ_DATABASE = os.path.join(DATABASE_PATH, "faq_database.json")
    LOAN_PRODUCTS_DB = os.path.join(DATABASE_PATH, "loan_products.json")
    CONVERSATION_LOGS = os.path.join(DATABASE_PATH, "conversation_logs.json")
    
    # API settings
    API_PREFIX = "/api"
    CORS_ORIGINS = ["http://localhost:5000", "http://127.0.0.1:5000"]
    
    # Loan settings
    PENALTY_RATE = 2.0  # Default penalty rate for missed payments
    MIN_CREDIT_SCORE = 300
    MAX_CREDIT_SCORE = 900
    
    # Chatbot settings
    MAX_HISTORY = 50  # Maximum conversation history to keep
    RESPONSE_TIMEOUT = 2  # Seconds