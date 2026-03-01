# 🏦 Chatbot Borrower - Complete Project Structure

## **Overall Architecture**

```
Frontend (HTML/CSS/JS) → Backend Server (Flask) → Chat Logic
```

---

## **FILE STRUCTURE**

### 📁 **backend/** (Python Flask Server)
- `src/app.py` - Main Flask server
- `src/chatbot.py` - Chat AI logic
- `src/faq_data.py` - FAQ database
- `config.py` - Configuration

### 📁 **frontend/** (User Interface)
- `index.html` - Main page (AI + FAQ + EMI + Eligibility)
- `style.css` - Styling for all pages
- `script.js` - JavaScript logic

### 📁 **data/** (Database Files)
- `faq_data.csv` - FAQ in CSV
- `loan_knowledge.json` - Loan info in JSON
- `loan_products.json` - Loan types & rates

---

## **CURRENT PAGE STRUCTURE (index.html)**

### ✅ **1. AI CHAT PAGE** (Default)
- **Left**: Large AI Avatar (Finova)
- **Right**: Chat messages + input
- **Action**: Click minimize arrow → Go to FAQ page

### ✅ **2. FAQ PAGE** (3-Panel Layout)
- **Left Panel**: Popular topics (Interest, Eligibility, Documents, Credit Score, Repayment)
- **Center Panel**: Chat interface with messages
- **Right Panel**: Topic-specific questions + search

### ✅ **3. EMI CALCULATOR PAGE**
- Input: Loan amount, interest rate, tenure, credit score
- Output: Monthly EMI, total interest, total payment
- Feature: Missed payment penalty calculator

### ✅ **4. ELIGIBILITY CHECKER PAGE**
- Input: Monthly income, age, credit score, existing EMI
- Output: Max loan amount, eligibility %age, interest rate
- Dynamic: Results based on credit score category

---

## **HOW IT WORKS**

### **1. AI Chat Flow (Main Page)**
```
User types message → 
  ↓
sendMessage() in script.js →
  ↓
Try to send to Flask backend (http://127.0.0.1:5000/api/chat) →
  ↓
If backend works: Get response from chatbot.py →
If backend fails: Use local fallback getResponse() →
  ↓
Display message in chat bubble
```

### **2. FAQ Chat Flow (FAQ Page)**
```
User clicks topic (e.g., "Interest") →
  ↓
loadQuestions() shows related questions in right panel →
  ↓
User types question OR clicks question from right panel →
  ↓
sendFAQMessage() searches faqDatabase array →
  ↓
Find matching FAQ entries →
  ↓
Display answer in center chat area
```

### **3. EMI Calculator Flow**
```
User enters: Loan Amount, Interest Rate, Tenure →
  ↓
calculateEMI() function →
  ↓
Formula: EMI = (P × R × (1+R)^N) / ((1+R)^N - 1)
where P=amount, R=monthly rate, N=months →
  ↓
Display: Monthly EMI, Total Interest, Total Payment
```

### **4. Eligibility Checker Flow**
```
User enters: Income, Age, Credit Score, Existing EMI →
  ↓
checkEligibility() function →
  ↓
Determine category based on credit score:
  - 800+: Excellent (60% of annual income)
  - 750-799: Good (50%)
  - 700-749: Fair (40%)
  - 650-699: Average (25%)
  - Below 650: Poor/Not Eligible →
  ↓
Calculate: Max Loan = Annual Income × Eligibility %
  ↓
Display: Eligibility status + Max loan amount + Interest rate
```

---

## **FRONTEND DATA STRUCTURE**

### **FAQ Database** (script.js line ~220)
```javascript
const faqDatabase = [
    {
        id: 1,
        question: "What are personal loan interest rates?",
        answer: "Personal loan interest rates range from 10.5% to 18% p.a...",
        emoji: "💰",
        category: "interest",
        keywords: ["interest", "rate", "personal loan"]
    },
    // ... more FAQs
]
```

### **Topics Generated From Categories**
- Interest (Personal, Home, Car, Education)
- Eligibility (for each loan type)
- Documents (for each loan type)

---

## **KEY FUNCTIONS**

### **Navigation**
- `navigateTo(page)` - Go to EMI or Eligibility page
- `goBack()` - Return to FAQ page
- `minimizeAI()` / `maximizeAI()` - Toggle AI page

### **FAQ**
- `loadTopics()` - Load categories from database
- `loadQuestions(category)` - Load questions for category
- `sendFAQMessage()` - Send message to FAQ chat
- `addFAQMessage(text, sender)` - Add message to chat

### **EMI Calculator**
- `calculateEMI()` - Calculate EMI amount
- `calculateMissedPayment()` - Calculate penalty

### **Eligibility**
- `checkEligibility()` - Check eligibility and max loan

### **Utilities**
- `toggleDarkMode()` - Enable/disable dark mode
- `getResponse(message)` - Fallback local responses

---

## **STYLING**

### **Color Scheme**
- Primary: `#667eea` (Purple-blue)
- Secondary: `#764ba2` (Purple)
- Accent: `#ff6b6b` (Red for user messages)
- Background: `#f4f6fb` (Light blue)
- Text: `#1e293b` (Dark slate)

### **Key CSS Classes**
- `.modern-layout` - 3-panel FAQ layout
- `.chat-panel` - Chat message area
- `.message` - Individual messages
- `.topic-btn` - Category buttons
- `.question-item` - Question list items

---

## **BACKEND FEATURES** (Python)

### **Flask Routes**
- `POST /api/chat` - Send message to chatbot
- `GET /api/loan-products` - Get loan rates
- `POST /api/calculate-emi` - Calculate EMI
- `GET /` - Serve index.html
- `GET /<filename>` - Serve frontend files

### **ChatBot Class** (chatbot.py)
- `get_response(message)` - Generate response
- `get_suggestions(message)` - Suggest related topics
- `load_csv_data()` - Load FAQ from CSV
- `load_json_data()` - Load FAQ from JSON

---

## **TROUBLESHOOTING**

### **Issue: Backend doesn't start**
- Check if Python 3.8+ installed
- Run: `pip install -r requirements.txt`
- Check port 5000 is free

### **Issue: FAQ not loading**
- Check if `faqDatabase` array has data in script.js
- Check browser console for JS errors

### **Issue: EMI calculation wrong**
- Verify formula: `EMI = (P × R × (1+R)^N) / ((1+R)^N - 1)`
- Check if monthly rate is calculated: `rate / (12 * 100)`

### **Issue: Eligibility showing error**
- Check credit score is 300-900
- Check income is positive number

---

## **NEXT STEPS TO IMPROVE**

1. ✅ Add backend chat API integration
2. ✅ Add EMI calculator
3. ✅ Add eligibility checker
4. ✅ Add dark mode
5. ⏳ Add user registration/login
6. ⏳ Save calculation history
7. ⏳ Email/SMS notifications
8. ⏳ Mobile responsive design

---

## **QUICK START**

1. **Start Backend:**
   ```bash
   cd chatbotBorrower
   python src/app.py
   ```

2. **Start Frontend:**
   - Open `frontend/index.html` in browser
   - Or open `http://localhost:5000`

3. **Test Pages:**
   - AI Chat: Default page
   - FAQ: Click minimize button
   - EMI: Click calculator icon
   - Eligibility: Click check mark icon

---

**Happy Coding! 🚀**
