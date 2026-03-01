import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

class TextProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Loan-specific stopwords to keep
        self.loan_keywords = {
            'loan', 'emi', 'interest', 'rate', 'credit', 'score', 'cibil',
            'eligibility', 'document', 'repayment', 'prepayment', 'foreclosure',
            'disbursement', 'tenure', 'fee', 'charges', 'processing', 'salary',
            'income', 'amount', 'approve', 'reject', 'default', 'npa'
        }
        
        # Common spelling mistakes mapping
        self.spelling_corrections = {
            'intrest': 'interest',
            'intrests': 'interest',
            'intrested': 'interest',
            'eligble': 'eligible',
            'eligibilty': 'eligibility',
            'documnt': 'document',
            'documnts': 'documents',
            'repament': 'repayment',
            'repaymnt': 'repayment',
            'prepaymnt': 'prepayment',
            'foreclosur': 'foreclosure',
            'disbursmnt': 'disbursement',
            'disbursment': 'disbursement',
            'tenur': 'tenure',
            'cibil': 'credit score',
            'cibl': 'credit score',
            'procesing': 'processing',
            'proc': 'processing',
            'elig': 'eligibility',
            'calclate': 'calculate',
            'calcu': 'calculate',
            'ammount': 'amount',
            'amnt': 'amount',
            'montly': 'monthly',
            'mnthly': 'monthly',
            'emmi': 'emi',
            'intrst': 'interest',
            'cred': 'credit',
            'scor': 'score'
        }
        
        # Currency and number patterns
        self.currency_pattern = re.compile(r'[₹$€]\s*(\d+(?:,\d{3})*(?:\.\d{2})?)')
        self.number_pattern = re.compile(r'\d+(?:,\d{3})*(?:\.\d+)?')
        
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep currency symbols
        text = re.sub(r'[^a-zA-Z0-9\s₹$€%.,?]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def correct_spelling(self, text):
        """Correct common spelling mistakes"""
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Check if word is in corrections dictionary
            if word in self.spelling_corrections:
                corrected_words.append(self.spelling_corrections[word])
            # Check for partial matches
            else:
                for misspelled, correct in self.spelling_corrections.items():
                    if misspelled in word or word in misspelled:
                        corrected_words.append(correct)
                        break
                else:
                    corrected_words.append(word)
        
        return ' '.join(corrected_words)
    
    def extract_numbers(self, text):
        """Extract all numbers from text"""
        numbers = []
        
        # Find currency amounts
        currency_matches = self.currency_pattern.findall(text)
        for match in currency_matches:
            numbers.append(float(match.replace(',', '')))
        
        # Find regular numbers
        number_matches = self.number_pattern.findall(text)
        for match in number_matches:
            numbers.append(float(match.replace(',', '')))
        
        return numbers
    
    def extract_loan_amount(self, text):
        """Extract loan amount from text"""
        amounts = self.extract_numbers(text)
        
        # Filter reasonable loan amounts (1,000 to 10,000,000)
        loan_amounts = [amt for amt in amounts if 1000 <= amt <= 10000000]
        
        return loan_amounts[0] if loan_amounts else None
    
    def tokenize(self, text):
        """Tokenize text into words"""
        try:
            return word_tokenize(text)
        except:
            return text.split()
    
    def remove_stopwords(self, tokens):
        """Remove stopwords but keep loan-specific keywords"""
        filtered_tokens = []
        for token in tokens:
            if token not in self.stop_words or token in self.loan_keywords:
                filtered_tokens.append(token)
        return filtered_tokens
    
    def stem_words(self, tokens):
        """Apply stemming to tokens"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatize_words(self, tokens):
        """Apply lemmatization to tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def extract_keywords(self, text, use_lemmatization=True):
        """Extract important keywords from text"""
        # Clean text
        text = self.clean_text(text)
        
        # Correct spelling
        text = self.correct_spelling(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Remove punctuation
        tokens = [token for token in tokens if token not in string.punctuation]
        
        # Remove short words
        tokens = [token for token in tokens if len(token) > 2]
        
        # Lemmatize or stem
        if use_lemmatization:
            tokens = self.lemmatize_words(tokens)
        else:
            tokens = self.stem_words(tokens)
        
        return tokens
    
    def get_pos_tags(self, text):
        """Get parts of speech tags"""
        tokens = self.tokenize(text)
        try:
            return nltk.pos_tag(tokens)
        except:
            return [(token, 'UNK') for token in tokens]
    
    def extract_intent_clues(self, text):
        """Extract clues for intent classification"""
        clues = {
            'calculation': ['calculate', 'emi', 'how much', 'compute', 'find out'],
            'eligibility': ['eligible', 'qualify', 'can i get', 'criteria', 'requirement'],
            'document': ['document', 'paper', 'upload', 'proof', 'need to submit'],
            'interest': ['interest', 'rate', 'apr', 'percentage', 'cost'],
            'repayment': ['repay', 'emi', 'pay', 'installment', 'monthly'],
            'prepayment': ['prepay', 'foreclosure', 'early', 'close', 'before time'],
            'fees': ['fee', 'charge', 'processing', 'penalty', 'late'],
            'credit_score': ['credit', 'cibil', 'score', 'rating', 'cibil score'],
            'disbursement': ['disburs', 'receive', 'credited', 'transfer', 'when get'],
            'tenure': ['tenure', 'duration', 'period', 'long', 'time'],
            'status': ['status', 'track', 'application', 'progress', 'where is'],
            'default': ['default', 'miss', 'skip', 'fail', 'npa']
        }
        
        text_lower = text.lower()
        detected_clues = []
        
        for intent, keywords in clues.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_clues.append(intent)
                    break
        
        return detected_clues
    
    def preprocess_for_matching(self, text):
        """Complete preprocessing pipeline for similarity matching"""
        # Clean text
        text = self.clean_text(text)
        
        # Correct spelling
        text = self.correct_spelling(text)
        
        # Extract keywords
        keywords = self.extract_keywords(text)
        
        # Join back to string
        processed_text = ' '.join(keywords)
        
        return processed_text, keywords