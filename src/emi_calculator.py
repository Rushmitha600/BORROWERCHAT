import math
import json

class EMICalculator:
    def __init__(self):
        self.loan_products = {
            'personal': {
                'name': 'Personal Loan',
                'interest_rate': 10.5,
                'min_amount': 10000,
                'max_amount': 2500000,
                'min_tenure': 12,
                'max_tenure': 60
            },
            'home': {
                'name': 'Home Loan',
                'interest_rate': 8.5,
                'min_amount': 500000,
                'max_amount': 10000000,
                'min_tenure': 12,
                'max_tenure': 360
            },
            'car': {
                'name': 'Car Loan',
                'interest_rate': 9.5,
                'min_amount': 100000,
                'max_amount': 5000000,
                'min_tenure': 12,
                'max_tenure': 84
            },
            'education': {
                'name': 'Education Loan',
                'interest_rate': 11.0,
                'min_amount': 50000,
                'max_amount': 5000000,
                'min_tenure': 12,
                'max_tenure': 180
            }
        }
    
    def calculate_emi(self, principal, annual_rate, tenure_months):
        if principal <= 0 or annual_rate <= 0 or tenure_months <= 0:
            return {'error': 'Invalid input parameters'}
        
        monthly_rate = annual_rate / (12 * 100)
        emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / (math.pow(1 + monthly_rate, tenure_months) - 1)
        
        total_payment = emi * tenure_months
        total_interest = total_payment - principal
        
        return {
            'emi': round(emi, 2),
            'total_interest': round(total_interest, 2),
            'total_payment': round(total_payment, 2),
            'principal': principal,
            'monthly_rate': round(monthly_rate * 100, 3)
        }
    
    def calculate_missed_payment_penalty(self, monthly_emi, months_missed=1, penalty_rate=2.0):
        penalty = monthly_emi * (penalty_rate / 100) * months_missed
        next_payment = monthly_emi + penalty
        
        return {
            'original_emi': monthly_emi,
            'months_missed': months_missed,
            'penalty_amount': round(penalty, 2),
            'next_payment': round(next_payment, 2),
            'penalty_rate': penalty_rate
        }
    
    def get_loan_products(self):
        return self.loan_products
    
    def get_loan_details(self, loan_type):
        return self.loan_products.get(loan_type, {})