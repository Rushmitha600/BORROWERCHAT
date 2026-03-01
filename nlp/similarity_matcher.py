import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import re
from text_processor import TextProcessor

class SimilarityMatcher:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.faq_vectors = None
        self.faq_questions = []
        self.faq_keywords = []
        self.faq_data = None
        
    def initialize_faqs(self, faqs):
        """Initialize FAQ data for matching"""
        self.faq_data = faqs
        self.faq_questions = [faq['question'] for faq in faqs]
        self.faq_keywords = [' '.join(faq['keywords']) for faq in faqs]
        
        # Prepare texts for vectorization
        all_texts = []
        for faq in faqs:
            # Combine question and keywords
            text = faq['question'] + ' ' + ' '.join(faq['keywords'])
            processed_text, _ = self.text_processor.preprocess_for_matching(text)
            all_texts.append(processed_text)
        
        # Fit vectorizer and transform
        if all_texts:
            self.faq_vectors = self.vectorizer.fit_transform(all_texts)
    
    def calculate_similarity_scores(self, query, method='hybrid'):
        """Calculate similarity scores using multiple methods"""
        if self.faq_vectors is None:
            return []
        
        # Preprocess query
        processed_query, query_keywords = self.text_processor.preprocess_for_matching(query)
        
        scores = []
        
        for idx, faq in enumerate(self.faq_data):
            score = 0
            methods_used = []
            
            if method in ['tfidf', 'hybrid']:
                # TF-IDF Cosine Similarity
                query_vector = self.vectorizer.transform([processed_query])
                tfidf_score = cosine_similarity(query_vector, self.faq_vectors[idx])[0][0]
                score += tfidf_score * 0.4  # 40% weight
                methods_used.append(f'tfidf:{tfidf_score:.2f}')
            
            if method in ['fuzzy', 'hybrid']:
                # Fuzzy matching on question
                fuzzy_q_score = fuzz.ratio(processed_query, self.faq_questions[idx].lower()) / 100
                fuzzy_partial_score = fuzz.partial_ratio(processed_query, self.faq_questions[idx].lower()) / 100
                fuzzy_token_score = fuzz.token_set_ratio(processed_query, self.faq_questions[idx].lower()) / 100
                
                fuzzy_score = max(fuzzy_q_score, fuzzy_partial_score, fuzzy_token_score)
                score += fuzzy_score * 0.3  # 30% weight
                methods_used.append(f'fuzzy:{fuzzy_score:.2f}')
            
            if method in ['keyword', 'hybrid']:
                # Keyword matching
                keyword_text = ' '.join(faq['keywords'])
                keyword_matches = 0
                for keyword in query_keywords:
                    if keyword in keyword_text or any(fuzz.ratio(keyword, k) > 80 for k in faq['keywords']):
                        keyword_matches += 1
                
                keyword_score = keyword_matches / max(len(query_keywords), 1) if query_keywords else 0
                score += keyword_score * 0.3  # 30% weight
                methods_used.append(f'keyword:{keyword_score:.2f}')
            
            scores.append({
                'index': idx,
                'faq_id': faq['id'],
                'question': faq['question'],
                'answer': faq['answer'],
                'category': faq['category'],
                'emoji': faq['emoji'],
                'score': score,
                'methods': methods_used
            })
        
        # Sort by score
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return scores
    
    def find_best_match(self, query, threshold=0.4):
        """Find best matching FAQ"""
        scores = self.calculate_similarity_scores(query)
        
        if scores and scores[0]['score'] >= threshold:
            best_match = scores[0]
            
            # Determine match quality
            if best_match['score'] >= 0.8:
                quality = 'exact'
            elif best_match['score'] >= 0.6:
                quality = 'high'
            elif best_match['score'] >= 0.4:
                quality = 'medium'
            else:
                quality = 'low'
            
            best_match['match_quality'] = quality
            best_match['match_score'] = best_match['score']
            
            return best_match
        
        return None
    
    def find_multiple_matches(self, query, top_k=3, threshold=0.3):
        """Find top K matching FAQs"""
        scores = self.calculate_similarity_scores(query)
        
        matches = []
        for score in scores[:top_k]:
            if score['score'] >= threshold:
                matches.append(score)
        
        return matches
    
    def extract_entities(self, query):
        """Extract entities like amount, tenure, rate from query"""
        entities = {}
        
        # Extract loan amount
        amount_patterns = [
            r'(?:rs\.?|inr|₹)\s*(\d+(?:,\d{3})*(?:\.\d+)?)',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:lakh|lacs|lac)',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:crore|crs)',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:thousand|k)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, query.lower())
            if match:
                amount = float(match.group(1).replace(',', ''))
                if 'lakh' in query.lower() or 'lac' in query.lower():
                    amount *= 100000
                elif 'crore' in query.lower() or 'cr' in query.lower():
                    amount *= 10000000
                elif 'thousand' in query.lower() or 'k' in query.lower():
                    amount *= 1000
                
                entities['amount'] = amount
        
        # Extract tenure
        tenure_patterns = [
            r'(\d+)\s*(?:year|yr|y)',
            r'(\d+)\s*(?:month|mon)'
        ]
        
        for pattern in tenure_patterns:
            match = re.search(pattern, query.lower())
            if match:
                value = int(match.group(1))
                if 'year' in pattern or 'yr' in pattern:
                    entities['tenure_years'] = value
                    entities['tenure_months'] = value * 12
                else:
                    entities['tenure_months'] = value
                    entities['tenure_years'] = value / 12
        
        # Extract interest rate
        rate_patterns = [
            r'(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*percent',
            r'rate[:\s]*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in rate_patterns:
            match = re.search(pattern, query.lower())
            if match:
                entities['interest_rate'] = float(match.group(1))
        
        # Extract credit score
        score_patterns = [
            r'cibil[:\s]*(\d+)',
            r'credit score[:\s]*(\d+)',
            r'score[:\s]*(\d+)'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, query.lower())
            if match:
                entities['credit_score'] = int(match.group(1))
        
        return entities
    
    def calculate_question_similarity(self, question1, question2):
        """Calculate similarity between two questions"""
        # Preprocess both questions
        q1_processed, _ = self.text_processor.preprocess_for_matching(question1)
        q2_processed, _ = self.text_processor.preprocess_for_matching(question2)
        
        # TF-IDF similarity
        vectors = self.vectorizer.fit_transform([q1_processed, q2_processed])
        tfidf_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        # Fuzzy similarity
        fuzzy_similarity = fuzz.ratio(q1_processed, q2_processed) / 100
        
        # Combined score
        similarity = (tfidf_similarity * 0.6) + (fuzzy_similarity * 0.4)
        
        return {
            'similarity': similarity,
            'tfidf_score': tfidf_similarity,
            'fuzzy_score': fuzzy_similarity
        }
    
    def find_similar_questions(self, query, faqs, threshold=0.3):
        """Find questions similar to query"""
        similar = []
        
        for faq in faqs:
            similarity_score = self.calculate_question_similarity(query, faq['question'])
            if similarity_score['similarity'] >= threshold:
                similar.append({
                    'faq_id': faq['id'],
                    'question': faq['question'],
                    'similarity': similarity_score['similarity'],
                    'details': similarity_score
                })
        
        # Sort by similarity
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar[:5]  # Return top 5
    
    def get_match_explanation(self, query, match):
        """Generate explanation for why this match was found"""
        explanation = []
        
        # Check if query contains keywords from the match
        query_keywords = set(self.text_processor.extract_keywords(query))
        faq_keywords = set(match.get('keywords', []))
        
        common_keywords = query_keywords.intersection(faq_keywords)
        if common_keywords:
            explanation.append(f"✓ Matched keywords: {', '.join(common_keywords)}")
        
        # Add match quality explanation
        if match['match_quality'] == 'exact':
            explanation.append("✓ This is an exact match to your question")
        elif match['match_quality'] == 'high':
            explanation.append("✓ Very similar to a question in our database")
        elif match['match_quality'] == 'medium':
            explanation.append("✓ Partially matches a common question")
        else:
            explanation.append("✓ This is the closest related question we found")
        
        return ' '.join(explanation)