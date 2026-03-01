import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os
from text_processor import TextProcessor

class IntentClassifier:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.classifier = None
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3))
        self.intents = [
            'greeting',
            'emi_calculation',
            'eligibility_check',
            'interest_rate_query',
            'document_query',
            'repayment_query',
            'prepayment_query',
            'credit_score_query',
            'fees_query',
            'disbursement_query',
            'tenure_query',
            'loan_status_query',
            'default_query',
            'balance_transfer',
            'topup_loan',
            'loan_against_property',
            'coapplicant_query',
            'moratorium_query',
            'special_loan_query',
            'general_faq',
            'unknown'
        ]
        
        # Training data for intent classification
        self.training_data = self._prepare_training_data()
        
    def _prepare_training_data(self):
        """Prepare training data for intent classification"""
        training_data = {
            'greeting': [
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
                'namaste', 'hola', 'greetings', 'howdy', 'whats up', 'sup'
            ],
            'emi_calculation': [
                'calculate emi', 'emi calculator', 'how much emi', 'monthly payment',
                'emi for 5 lakhs', 'what will be my emi', 'calculate monthly installment',
                'emi amount', 'how to calculate emi', 'emi formula'
            ],
            'eligibility_check': [
                'am i eligible', 'check eligibility', 'can i get loan', 'qualify for loan',
                'eligibility criteria', 'minimum salary for loan', 'who can apply',
                'do i qualify', 'eligibility requirements', 'check if i am eligible'
            ],
            'interest_rate_query': [
                'interest rate', 'what is the interest', 'how much interest', 'rate of interest',
                'loan interest', 'interest charges', 'interest percentage', 'apr',
                'current interest rates', 'interest rate today'
            ],
            'document_query': [
                'documents required', 'what documents', 'paperwork needed', 'upload documents',
                'document list', 'required proofs', 'what to submit', 'identity proof',
                'address proof', 'income proof'
            ],
            'repayment_query': [
                'how to repay', 'repayment options', 'pay emi', 'payment methods',
                'how to pay loan', 'emi payment', 'repayment schedule', 'pay online',
                'autodebit', 'repayment tenure'
            ],
            'prepayment_query': [
                'prepayment', 'foreclosure', 'close loan early', 'pay before time',
                'prepayment charges', 'part prepayment', 'full prepayment', 'early settlement',
                'how to close loan', 'prepayment rules'
            ],
            'credit_score_query': [
                'credit score', 'cibil score', 'good credit score', 'improve credit score',
                'check credit score', 'credit rating', 'cibil report', 'minimum credit score',
                'how to increase cibil', 'credit score range'
            ],
            'fees_query': [
                'processing fee', 'loan charges', 'fees and charges', 'late payment fee',
                'bounce charges', 'prepayment charges', 'administrative fee',
                'what are the charges', 'fee structure', 'hidden charges'
            ],
            'disbursement_query': [
                'disbursement', 'when will i get money', 'loan credited', 'disbursement time',
                'loan amount transfer', 'receive loan amount', 'disbursement process',
                'how long for disbursement', 'instant disbursement'
            ],
            'tenure_query': [
                'loan tenure', 'maximum tenure', 'loan period', 'repayment period',
                'how long can i take', 'tenure options', 'minimum tenure', 'extend tenure',
                'tenure for personal loan', 'home loan tenure'
            ],
            'loan_status_query': [
                'loan status', 'application status', 'track loan', 'check status',
                'where is my loan', 'application progress', 'status of my application',
                'how to check status', 'loan approval status'
            ],
            'default_query': [
                'default on loan', 'miss emi', 'skip payment', 'what if i dont pay',
                'consequences of default', 'npa', 'loan default', 'failed to pay',
                'late payment consequences', 'cibil impact'
            ],
            'balance_transfer': [
                'balance transfer', 'loan transfer', 'transfer to another bank',
                'refinance loan', 'switch loan', 'balance transfer benefit',
                'balance transfer charges', 'transfer my loan'
            ],
            'topup_loan': [
                'top up loan', 'additional loan', 'extra loan amount', 'topup on existing loan',
                'increase loan amount', 'top up eligibility', 'top up interest rate'
            ],
            'loan_against_property': [
                'loan against property', 'lap', 'property loan', 'mortgage loan',
                'loan on house', 'property as collateral', 'secured loan property'
            ],
            'coapplicant_query': [
                'co applicant', 'joint loan', 'add co applicant', 'co borrower',
                'joint applicant', 'spouse as co applicant', 'co applicant income'
            ],
            'moratorium_query': [
                'moratorium', 'payment holiday', 'emi holiday', 'skip emi',
                'pause emi', 'defer payment', 'moratorium period'
            ],
            'special_loan_query': [
                'loan for pensioner', 'senior citizen loan', 'farmer loan',
                'agriculture loan', 'kisan credit card', 'pensioner loan',
                'student loan', 'education loan'
            ],
            'general_faq': [
                'what is personal loan', 'types of loans', 'secured vs unsecured',
                'loan meaning', 'how loan works', 'about loan', 'loan information'
            ]
        }
        
        return training_data
    
    def train_classifier(self):
        """Train the intent classifier"""
        X_train = []
        y_train = []
        
        for intent, examples in self.training_data.items():
            for example in examples:
                processed_text, _ = self.text_processor.preprocess_for_matching(example)
                X_train.append(processed_text)
                y_train.append(intent)
        
        # Create pipeline
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 3))),
            ('clf', MultinomialNB())
        ])
        
        # Train
        self.classifier.fit(X_train, y_train)
        
        return self.classifier
    
    def predict_intent(self, text, confidence_threshold=0.4):
        """Predict intent of user message"""
        # Preprocess text
        processed_text, keywords = self.text_processor.preprocess_for_matching(text)
        
        # Check for explicit intent clues first
        clues = self.text_processor.extract_intent_clues(text)
        
        # If classifier not trained, train it
        if self.classifier is None:
            self.train_classifier()
        
        # Get prediction probabilities
        try:
            probs = self.classifier.predict_proba([processed_text])[0]
            max_prob = max(probs)
            predicted_intent = self.classifier.classes_[np.argmax(probs)]
            
            # Override with explicit clues if confidence is low
            if clues and max_prob < confidence_threshold:
                # Map clue to intent
                clue_to_intent = {
                    'calculation': 'emi_calculation',
                    'eligibility': 'eligibility_check',
                    'document': 'document_query',
                    'interest': 'interest_rate_query',
                    'repayment': 'repayment_query',
                    'prepayment': 'prepayment_query',
                    'fees': 'fees_query',
                    'credit_score': 'credit_score_query',
                    'disbursement': 'disbursement_query',
                    'tenure': 'tenure_query',
                    'status': 'loan_status_query',
                    'default': 'default_query'
                }
                
                for clue in clues:
                    if clue in clue_to_intent:
                        predicted_intent = clue_to_intent[clue]
                        max_prob = 0.7  # High confidence for explicit clues
                        break
            
            return {
                'intent': predicted_intent,
                'confidence': float(max_prob),
                'keywords': keywords,
                'clues': clues
            }
            
        except Exception as e:
            print(f"Error predicting intent: {e}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'keywords': keywords,
                'clues': clues
            }
    
    def get_intent_from_patterns(self, text):
        """Rule-based intent detection as fallback"""
        text_lower = text.lower()
        
        # EMI calculation patterns
        if re.search(r'calculate|emi|monthly payment|installment', text_lower):
            if re.search(r'emi|installment', text_lower):
                return 'emi_calculation'
        
        # Eligibility patterns
        if re.search(r'eligible|qualify|can i get|can i apply', text_lower):
            return 'eligibility_check'
        
        # Interest rate patterns
        if re.search(r'interest|rate|apr|percentage', text_lower):
            return 'interest_rate_query'
        
        # Document patterns
        if re.search(r'document|paper|proof|upload|submit', text_lower):
            return 'document_query'
        
        # Repayment patterns
        if re.search(r'repay|payment|pay|emi|installment', text_lower):
            return 'repayment_query'
        
        # Prepayment patterns
        if re.search(r'prepay|foreclosure|close loan|early', text_lower):
            return 'prepayment_query'
        
        # Credit score patterns
        if re.search(r'credit score|cibil|credit rating', text_lower):
            return 'credit_score_query'
        
        # Fees patterns
        if re.search(r'fee|charge|cost|processing fee', text_lower):
            return 'fees_query'
        
        # Default to general FAQ
        return 'general_faq'
    
    def save_model(self, filepath='models/intent_classifier.pkl'):
        """Save trained model to file"""
        if self.classifier:
            joblib.dump(self.classifier, filepath)
            return True
        return False
    
    def load_model(self, filepath='models/intent_classifier.pkl'):
        """Load trained model from file"""
        if os.path.exists(filepath):
            self.classifier = joblib.load(filepath)
            return True
        return False