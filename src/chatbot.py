import difflib
import re
import csv
import os
import json
from faq_data import FAQData


class ChatBot:

    # ================= INIT =================
    def __init__(self):
        self.faq_data = FAQData()
        self.base_faqs = self.faq_data.get_all_faqs()

        self.csv_faqs = self.load_csv_data()
        self.json_faqs = self.load_json_data()

        self.all_faqs = self.base_faqs + self.csv_faqs + self.json_faqs

        self.greetings = [
            "hi", "hello", "hey",
            "good morning", "good afternoon",
            "good evening", "good night",
            "namaste", "hlo"
        ]

        # polite/auxiliary intents
        self.thanks = ["thank", "thanks", "thx", "thank you", "much appreciated", "tq"]
        self.apologies = ["sorry", "apologies", "pardon"]
        self.farewells = ["bye", "goodbye", "see you", "take care"]

        # ========== Mixed Language Patterns ==========
        self.mixed_patterns = {
            "emi": ["emi", "installment", "monthly payment"],
            "calculate": ["calculate", "cheppu", "entha", "kavali", "chey"],
            "interest": ["interest", "rate", "percent", "%"],
            "loan": ["loan", "appu"],
            "eligible": ["eligible", "vasthunda", "raada", "possible"],
            "documents": ["documents", "docs", "papers", "files"],
            "credit": ["credit", "cibil", "score"],
            "foreclosure": ["close", "prepay", "foreclosure", "early", "penalty"],
            "processing": ["processing", "fee", "charges"]
        }

        # ========== Spelling Mistakes Dictionary ==========
        self.spelling_mistakes = {
            # EMI related
            "emi": ["emmi", "emi", "emmy", "emee", "e m i"],
            "installment": ["instalment", "installement", "installment", "insallment", "emis"],
            
            # Interest related
            "interest": ["interest", "intrest", "interst", "intrest", "interst", "intrust"],
            "rate": ["rate", "rte", "reat", "ret"],
            "percent": ["percent", "persent", "pct", "percentage", "prcent"],
            
            # Document related
            "document": ["document", "documant", "docment", "docs", "docks", "dokument"],
            
            # Credit related
            "credit": ["credit", "creadit", "creedit", "creditt", "kredit"],
            "cibil": ["cibil", "cible", "cibill", "sibil", "cibul"],
            "score": ["score", "skore", "scor", "scores"],
            
            # Eligibility related
            "eligibility": ["eligibility", "eligebility", "elgibility", "eligible", "elegible"],
            "eligible": ["eligible", "elegible", "elgible", "eligble"],
            "salary": ["salary", "selary", "slary", "salery"],
            "income": ["income", "imcome", "incom", "incone"],
            
            # General loan terms
            "loan": ["loan", "lone", "loen"],
            "amount": ["amount", "amout", "ammount", "amont"],
            "tenure": ["tenure", "tenur", "tenor", "tenure"],
            "months": ["months", "monts", "moths", "monhs"],
            "years": ["years", "yrs", "year", "yeras"],
            
            # Calculation related
            "calculate": ["calculate", "calcuate", "calc", "calulate", "calclate"],
            "formula": ["formula", "formulla", "formla", "formual"],
            
            # Questions
            "what": ["what", "wat", "wht", "wot"],
            "how": ["how", "hw", "hou"],
            "meaning": ["meaning", "menaing", "meening", "mining"],
            "full form": ["full form", "fullform", "ful form", "fool form"],
            "difference": ["difference", "diffrence", "diference", "diff"]
        }

        # Build reverse mapping for quick lookup
        self.correct_words = {}
        for correct, mistakes in self.spelling_mistakes.items():
            for mistake in mistakes:
                self.correct_words[mistake] = correct

    # ================= LOAD CSV =================
    def load_csv_data(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "data", "faq_data.csv")

        data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        data.append({
                            "question": row[0].strip(),
                            "answer": row[1].strip()
                        })
        return data

    # ================= LOAD JSON =================
    def load_json_data(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "data", "loan_knowledge.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        return []

    # ================= CLEAN TEXT =================
    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    # ========== Fix spelling mistakes ==========
    def fix_spelling(self, text):
        words = text.lower().split()
        corrected_words = []
        
        for word in words:
            # Check if word is in our spelling mistakes dictionary
            if word in self.correct_words:
                corrected_words.append(self.correct_words[word])
            else:
                # Try fuzzy matching for words not in dictionary
                best_match = difflib.get_close_matches(word, self.correct_words.keys(), n=1, cutoff=0.8)
                if best_match:
                    corrected_words.append(self.correct_words[best_match[0]])
                else:
                    corrected_words.append(word)
        
        return ' '.join(corrected_words)

    # ================= CONVERT LAKH/CR =================
    def convert_amounts(self, text):
        text = text.lower()

        text = re.sub(r'(\d+)\s*lakh', lambda m: str(int(m.group(1)) * 100000), text)
        text = re.sub(r'(\d+)\s*cr', lambda m: str(int(m.group(1)) * 10000000), text)
        text = re.sub(r'(\d+)l\b', lambda m: str(int(m.group(1)) * 100000), text)
        text = re.sub(r'(\d+)k\b', lambda m: str(int(m.group(1)) * 1000), text)

        return text

    # ================= EXTRACT NUMBERS =================
    def extract_numbers(self, message):
        message = self.convert_amounts(message)
        numbers = re.findall(r'\d+\.?\d*', message)
        return list(map(float, numbers))

    # ================= EMI =================
    def calculate_emi(self, principal, rate, tenure_months):
        if principal == 0 or rate == 0 or tenure_months == 0:
            return 0

        monthly_rate = rate / (12 * 100)
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / \
              ((1 + monthly_rate) ** tenure_months - 1)

        return round(emi, 2)

    # ================= SIMPLE INTEREST =================
    def calculate_simple_interest(self, p, r, t):
        return round((p * r * t) / 100, 2)

    # ================= FAQ MATCH =================
    def match_faq(self, message):
        cleaned = self.clean_text(message)
        questions = [self.clean_text(faq["question"]) for faq in self.all_faqs]

        match = difflib.get_close_matches(cleaned, questions, n=1, cutoff=0.7)

        if match:
            for faq in self.all_faqs:
                if self.clean_text(faq["question"]) == match[0]:
                    return faq["answer"]
        return None

    # ================= Mixed Language Intent Detection =================
    def detect_mixed_intent(self, message):
        msg = message.lower()
        
        # Check for EMI calculation patterns with numbers
        if re.search(r'(\d+)\s*(l|lak|la|c)?\s*(emi|installment)', msg) or \
           re.search(r'emi\s*(\d+)', msg) or \
           re.search(r'(\d+)\s*(l|lak|la)\s*(\d+)', msg):
            return "emi_calculation"
        
        # Check for interest calculation
        if re.search(r'interest\s*(\d+)', msg) or \
           re.search(r'simple interest', msg):
            return "interest_calculation"
        
        # Check for eligibility with income
        if re.search(r'(\d+)\s*(salary|income)\s*(\d+)', msg) or \
           re.search(r'(\d+)\s*(l|lak|la)\s*(possible|eligible)', msg):
            return "eligibility_check"
        
        return None

    # ================= INTENT DETECTION =================
    def detect_intent(self, message):
        # First fix spelling mistakes
        corrected_message = self.fix_spelling(message)
        msg = corrected_message.lower()

        # normalize common abbreviations
        const_map = {
            'gm': 'good morning', 'gn': 'good night', 'tq': 'thank you',
            'tnx': 'thanks', 'thq': 'thank you', 'thx': 'thanks',
            'sry': 'sorry', 'evng': 'evening', 'hlo': 'hello',
            'helo': 'hello', 'pls': 'please', 'plz': 'please'
        }
        for short, full in const_map.items():
            msg = re.sub(rf"\b{re.escape(short)}\b", full, msg)

        # First check for mixed language patterns
        mixed_intent = self.detect_mixed_intent(message)
        if mixed_intent:
            return mixed_intent

        # Check for general loan query
        if msg.strip() in ["loan", "loan?", "loans", "what is loan"]:
            return "general_loan"

        # Check for meaning queries
        if "meaning" in msg or "definition" in msg:
            if "eligibility" in msg or "eligible" in msg:
                return "eligibility_meaning"
            if "emi" in msg:
                return "emi_meaning"
            if "interest" in msg:
                return "interest_meaning"
            if "credit" in msg or "cibil" in msg:
                return "credit_meaning"
            if "document" in msg:
                return "document_meaning"

        # Check for formula queries
        if "formula" in msg:
            if "interest" in msg or "simple interest" in msg:
                return "interest_formula"
            if "emi" in msg:
                return "emi_formula"

        if any(greet in msg for greet in self.greetings):
            return "greeting"

        if any(th in msg for th in self.thanks):
            return "thanks"

        if any(ap in msg for ap in self.apologies):
            return "apology"

        if any(fw in msg for fw in self.farewells):
            return "farewell"

        # Better EMI detection
        emi_patterns = ["emi", "installment", "monthly payment"]
        if any(pattern in msg for pattern in emi_patterns):
            return "emi"

        if "interest" in msg:
            return "interest"

        # Eligibility detection
        if any(word in msg for word in ["eligible", "eligibility", "salary", "income", "possible"]):
            return "eligibility"

        if "document" in msg or "docs" in msg:
            return "documents"

        if "credit" in msg or "cibil" in msg or "score" in msg:
            return "credit"

        # Specific loan types
        if "personal loan" in msg:
            return "personal_loan"
        if "home loan" in msg or "housing loan" in msg:
            return "home_loan"
        if "car loan" in msg or "auto loan" in msg:
            return "car_loan"
        if "education loan" in msg or "student loan" in msg:
            return "education_loan"

        # Foreclosure/Prepayment detection
        if any(word in msg for word in ["close", "prepay", "foreclosure", "early", "penalty"]):
            return "foreclosure"

        # Processing fee detection
        if "processing" in msg or "fee" in msg or "charges" in msg:
            return "processing"

        return "general"

    # ================= MAIN RESPONSE =================
    def get_response(self, message):

        # 🔥 1️⃣ FAQ FIRST (VERY IMPORTANT)
        faq_response = self.match_faq(message)
        if faq_response:
            return faq_response

        intent = self.detect_intent(message)
        numbers = self.extract_numbers(message)
        msg_lower = message.lower()

        # ===== Handle "eligibility meaning?" =====
        if intent == "eligibility_meaning" or "eligibility meaning" in msg_lower:
            return ("📋 **Eligibility Meaning**\n\n"
                    "Eligibility means whether you qualify for a loan based on certain criteria.\n\n"
                    "**Key Eligibility Factors:**\n"
                    "• Age: 21-60 years\n"
                    "• Income: Minimum ₹15,000-25,000/month\n"
                    "• Credit Score: 650+\n"
                    "• Employment: 1+ years experience\n\n"
                    "**Example:**\n"
                    "To check if you're eligible for ₹20 lakh loan with ₹75,000 salary, ask:\n"
                    "'I earn 75000 per month. Can I get 20 lakh loan?'")

        # ===== Handle eligibility queries with clean formatting =====
        if intent == "eligibility" or intent == "eligibility_check" or ("earn" in msg_lower and "loan" in msg_lower):
            if len(numbers) >= 2:
                # Sort numbers to identify income (smaller) and loan amount (larger)
                sorted_nums = sorted(numbers)
                monthly_income = sorted_nums[0]
                loan_amount = sorted_nums[-1]

                # Calculate estimated EMI (assuming 10% rate for 20 years)
                estimated_emi = self.calculate_emi(loan_amount, 10, 240)
                max_emi = monthly_income * 0.6  # 60% of income rule

                if estimated_emi <= max_emi:
                    return (f"✅ **Eligibility Result**\n\n"
                            f"1. **Monthly Income:** ₹{monthly_income:,.0f}\n"
                            f"2. **Requested Loan:** ₹{loan_amount:,.0f}\n"
                            f"3. **Estimated EMI:** ₹{estimated_emi:,.0f} per month\n"
                            f"4. **Maximum EMI Allowed:** ₹{max_emi:,.0f} (60% of income)\n\n"
                            f"✅ **You may be eligible!**\n\n"
                            f"Your estimated EMI falls within the 60% income limit.\n"
                            f"Final approval depends on your credit score, age, and existing loans.")
                else:
                    return (f"❌ **Eligibility Result**\n\n"
                            f"1. **Monthly Income:** ₹{monthly_income:,.0f}\n"
                            f"2. **Requested Loan:** ₹{loan_amount:,.0f}\n"
                            f"3. **Estimated EMI:** ₹{estimated_emi:,.0f} per month\n"
                            f"4. **Maximum EMI Allowed:** ₹{max_emi:,.0f} (60% of income)\n\n"
                            f"❌ **You may not be eligible** for this loan amount.\n\n"
                            f"Consider a lower loan amount. Estimated max qualifier: ₹{monthly_income * 10:,.0f}.")
            
            # If only income provided, give general guidance
            elif len(numbers) == 1:
                income = numbers[0]
                return (f"📊 **Eligibility Guide**\n\n"
                        f"• Monthly Income: ₹{income:,.0f}\n"
                        f"• Estimated Loan Capacity: Up to ₹{income * 12:,.0f}\n"
                        f"• Estimated EMI Capacity: ₹{income * 0.6:,.0f} per month\n\n"
                        f"Please specify the loan amount you want, for example:\n"
                        f"'I earn {income:,.0f} per month. Can I get 20 lakh loan?'")

        # ===== Handle "Simple interest formula?" =====
        if intent == "interest_formula" or "simple interest formula" in msg_lower:
            return ("📐 **Simple Interest Formula**\n\n"
                    "**Formula:** SI = (P × R × T) / 100\n\n"
                    "Where:\n"
                    "• **P** = Principal - Initial loan amount\n"
                    "• **R** = Rate of interest - Annual interest rate\n"
                    "• **T** = Time - Time period in years\n\n"
                    "**Example:**\n"
                    "For ₹1,00,000 at 10% for 2 years:\n"
                    "SI = (100000 × 10 × 2) / 100 = ₹20,000\n\n"
                    "**Total Amount = Principal + Interest**\n"
                    "= ₹1,00,000 + ₹20,000 = ₹1,20,000\n\n"
                    "Try it yourself: 'interest 500000 10 2'")

        # ===== Handle general "interest" without formula =====
        if intent == "interest" and "formula" not in msg_lower:
            if len(numbers) >= 3:
                p, r, t = numbers[:3]
                si = self.calculate_simple_interest(p, r, t)
                return f"📊 Simple Interest on ₹{p:,.0f} at {r}% for {t} years = ₹{si:,.0f}."
            return "Interest is the extra amount charged by lender for borrowing money. Ask for 'simple interest formula' to learn how to calculate it."

        # ===== Handle EMI calculation queries =====
        if intent == "emi_calculation" and len(numbers) >= 3:
            if len(numbers) == 3:
                p, r, t = numbers
                emi = self.calculate_emi(p, r, t)
                return (f"💰 **EMI Calculation**\n\n"
                        f"• Loan Amount: ₹{p:,.0f}\n"
                        f"• Interest Rate: {r}%\n"
                        f"• Tenure: {t:.0f} months\n"
                        f"• Monthly EMI: ₹{emi:,.0f}")
            elif len(numbers) >= 3:
                # Sort to identify: smallest is rate, largest is principal
                sorted_nums = sorted(numbers)
                if len(sorted_nums) >= 3:
                    p = sorted_nums[-1]  # largest is principal
                    r = sorted_nums[0]    # smallest is rate
                    t = sorted_nums[1] if len(sorted_nums) > 2 else 12
                    
                    # Adjust if rate seems too high (interest rate is usually under 30%)
                    if r > 30 and r < p/10:
                        r = sorted_nums[1]
                        p = sorted_nums[-1]
                    
                    emi = self.calculate_emi(p, r, t)
                    return (f"💰 **EMI Calculation**\n\n"
                            f"• Loan Amount: ₹{p:,.0f}\n"
                            f"• Interest Rate: {r}%\n"
                            f"• Tenure: {t:.0f} months\n"
                            f"• Monthly EMI: ₹{emi:,.0f}")

        # -------- GREETING --------
        if intent == "greeting":
            lowered = message.lower()
            if "good morning" in lowered:
                return "Good morning! I'm your loan assistant. How can I help you today?"
            if "good afternoon" in lowered:
                return "Good afternoon! I'm your loan assistant. How can I help you today?"
            if "good evening" in lowered:
                return "Good evening! I'm your loan assistant. How can I help you today?"
            if "good night" in lowered:
                return "Good night! Rest well and feel free to ask if you have loan questions."
            return "Hello! I'm your loan assistant. How can I help you today?"

        # -------- THANKS --------
        if intent == "thanks":
            return "You're welcome! 😊 Glad to help."

        # -------- APOLOGY --------
        if intent == "apology":
            return "No worries at all! Let me know if you have any questions."

        # -------- FAREWELL --------
        if intent == "farewell":
            return "Goodbye! Feel free to come back if you need more loan help."

        # -------- GENERAL LOAN --------
        if intent == "general_loan":
            return ("🏦 **Loan Information**\n\n"
                    "A loan is money borrowed from a bank or financial institution that you repay with interest over time.\n\n"
                    "**Common Loan Types:**\n"
                    "💰 Personal Loan - For personal expenses\n"
                    "🏠 Home Loan - For buying/constructing house\n"
                    "🚗 Car Loan - For vehicle purchase\n"
                    "🎓 Education Loan - For studies\n\n"
                    "**What would you like to know?**\n"
                    "• Interest rates (e.g., 'personal loan interest')\n"
                    "• Eligibility (e.g., 'home loan eligibility')\n"
                    "• Documents (e.g., 'car loan documents')\n"
                    "• EMI calculation (e.g., 'emi for 5 lakh 10% 5 years')")

        # -------- PERSONAL LOAN --------
        if intent == "personal_loan":
            return ("💰 **Personal Loan**\n\n"
                    "• Interest Rates: 10.5% - 18%\n"
                    "• Eligibility: Age 21-60, Income ₹20,000+/month, Credit Score 650+\n"
                    "• Documents: Aadhar, PAN, Salary slips, Bank statements\n"
                    "• Max Amount: Up to ₹25 Lakhs\n\n"
                    "Ask me about EMI calculation or specific bank rates!")

        # -------- HOME LOAN --------
        if intent == "home_loan":
            return ("🏠 **Home Loan**\n\n"
                    "• Interest Rates: 8.5% - 9.8%\n"
                    "• Eligibility: Age 21-65, Income ₹25,000+/month, Credit Score 650+\n"
                    "• Documents: Property papers, Income proof, IT returns\n"
                    "• Max Amount: Up to ₹1 Crore\n\n"
                    "Women borrowers get 0.05% concession!")

        # -------- CAR LOAN --------
        if intent == "car_loan":
            return ("🚗 **Car Loan**\n\n"
                    "• Interest Rates: 9.25% - 15%\n"
                    "• New Cars: 8.75% - 13.5%\n"
                    "• Used Cars: 12% - 16.5%\n"
                    "• EV Vehicles: 0.5% concession\n"
                    "• Documents: Aadhar, PAN, Income proof, Car quotation")

        # -------- EDUCATION LOAN --------
        if intent == "education_loan":
            return ("🎓 **Education Loan**\n\n"
                    "• Interest Rates: 8.85% - 16%\n"
                    "• India Studies: 8.85% - 12.5%\n"
                    "• Abroad Studies: 10.5% - 15%\n"
                    "• No collateral up to ₹4 Lakhs\n"
                    "• Merit scholarship: 1% off for 90%+ scores")

        # -------- EMI --------
        if intent == "emi":
            if len(numbers) >= 3:
                principal = numbers[0]
                rate = numbers[1]
                tenure = int(numbers[2])
                emi = self.calculate_emi(principal, rate, tenure)
                return (f"💰 **EMI Calculation**\n\n"
                        f"• Loan Amount: ₹{principal:,.0f}\n"
                        f"• Interest Rate: {rate}%\n"
                        f"• Tenure: {tenure} months\n"
                        f"• Monthly EMI: ₹{emi:,.0f}")
            return "EMI (Equated Monthly Installment) is the fixed monthly payment you make to repay a loan."

        # -------- DOCUMENTS --------
        if intent == "documents":
            return ("📄 **Required Documents**\n\n"
                    "• ID proof: Aadhar card, PAN card\n"
                    "• Address proof: Aadhar, Utility bills\n"
                    "• Income proof: Salary slips (3 months), IT returns\n"
                    "• Bank statements: Last 6 months\n"
                    "• Photos: 2 passport size\n\n"
                    "For specific loan types, ask:\n"
                    "'personal loan documents' or 'home loan documents'")

        # -------- CREDIT --------
        if intent == "credit":
            if numbers:
                score = numbers[0]
                if score >= 750:
                    return f"✅ Credit score {score:.0f} is **Excellent**! You'll get best loan rates."
                elif score >= 700:
                    return f"👍 Credit score {score:.0f} is **Good**. You'll likely get approved."
                elif score >= 650:
                    return f"⚠️ Credit score {score:.0f} is **Fair**. Approval possible with slightly higher rates."
                else:
                    return f"❌ Credit score {score:.0f} is **Low**. Consider improving before applying."
            return ("📊 **Credit Score Guide**\n\n"
                    "• 750+ : Excellent - Best rates\n"
                    "• 700-749: Good - Easy approval\n"
                    "• 650-699: Fair - May get approval\n"
                    "• Below 650: Poor - Difficult to get loans\n\n"
                    "To check your score: 'credit score 750'")

        # -------- FORECLOSURE --------
        if intent == "foreclosure":
            return ("🏁 **Loan Foreclosure / Prepayment**\n\n"
                    "You can close your loan early by paying the remaining amount.\n\n"
                    "**Charges:**\n"
                    "• Floating rate loans: **No charges**\n"
                    "• Fixed rate loans: 2-5% of outstanding amount\n\n"
                    "**Benefits:**\n"
                    "• Save on future interest\n"
                    "• Get NOC from bank\n\n"
                    "Contact your bank for exact calculation!")

        # -------- PROCESSING FEE --------
        if intent == "processing":
            return ("💰 **Processing Fee**\n\n"
                    "• Amount: 0.5% to 2% of loan amount\n"
                    "• Payment: At the time of application\n"
                    "• Refund: Non-refundable if loan rejected\n\n"
                    "**Example:**\n"
                    "For ₹5 Lakh loan, fee = ₹2,500 to ₹10,000\n\n"
                    "Some banks waive fee during special offers!")

        # -------- AUTO SIMPLE INTEREST --------
        if len(numbers) == 3:
            p, r, t = numbers
            si = self.calculate_simple_interest(p, r, t)
            return f"📊 Simple Interest on ₹{p:,.0f} at {r}% for {t} years = ₹{si:,.0f}."

        return "I specialize in loan queries. Ask about EMI, interest, eligibility, documents, credit score, foreclosure, or processing fees."

    # Suggestions
    def get_suggestions(self, message):
        return [faq['question'] for faq in self.all_faqs[:3]]