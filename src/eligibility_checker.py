class EligibilityChecker:
    def __init__(self):
        self.credit_score_ranges = {
            'poor': (300, 599),
            'fair': (600, 699),
            'good': (700, 799),
            'excellent': (800, 900)
        }
        
    def check_credit_score(self, score):
        if score < 300 or score > 900:
            return {
                'status': 'invalid',
                'message': 'Please enter a valid credit score between 300 and 900',
                'color': 'gray'
            }
        
        if score < 600:
            return {
                'status': 'not_eligible',
                'message': 'Not Eligible',
                'color': 'red',
                'details': 'Sorry, you are not eligible for loans at this time. Consider improving your credit score.'
            }
        elif score >= 800:
            return {
                'status': 'eligible',
                'message': 'Eligible',
                'color': 'green',
                'details': 'Congratulations! You are eligible for the best loan rates.'
            }
        else:
            return {
                'status': 'moderate',
                'message': 'Moderate Eligibility',
                'color': 'orange',
                'details': 'You have moderate eligibility. Please contact our team for assistance.'
            }
    
    def get_loan_suggestions(self, credit_score, income=None):
        suggestions = []
        
        if credit_score >= 750:
            suggestions.append({
                'type': 'personal',
                'max_amount': 2500000,
                'interest_rate': 9.5
            })
            suggestions.append({
                'type': 'home',
                'max_amount': 10000000,
                'interest_rate': 8.0
            })
        elif credit_score >= 650:
            suggestions.append({
                'type': 'personal',
                'max_amount': 1000000,
                'interest_rate': 11.5
            })
            suggestions.append({
                'type': 'car',
                'max_amount': 3000000,
                'interest_rate': 10.5
            })
        else:
            suggestions.append({
                'type': 'education',
                'max_amount': 500000,
                'interest_rate': 12.5
            })
        
        return suggestions