// ============================================
// COMPLETE WORKING LOANFAQ CHATBOT
// All original logic preserved WITH BACKEND API
// ============================================

console.log('Borrower Assistant AI - Loading...');

// State Management
let state = {
    activeCategory: 'all',
    faqs: [],
    messages: [],
    isDarkMode: false,
    isTyping: false,
    currentLoanType: 'none'
};

// DOM Elements
const elements = {
    messageInput: document.getElementById('messageInput'),
    sendBtn: document.getElementById('sendBtn'),
    messagesContainer: document.getElementById('messagesContainer'),
    questionsList: document.getElementById('questionsList'),
    chatMessages: document.getElementById('chatMessages'),
    chatInput: document.getElementById('chatInput'),
    typingIndicator: document.getElementById('typingIndicator'),
    currentTime: document.getElementById('currentTime'),
    timeGreeting: document.getElementById('timeGreeting'),
    questionsCount: document.getElementById('questionsCount'),
    totalFAQs: document.getElementById('totalFAQs'),
    faqSearch: document.getElementById('faqSearch'),
    themeToggle: document.getElementById('themeToggle')
};

// ============================================
// FAQ DATABASE (Your Original FAQ Data)
// ============================================

const faqDatabase = [
    {
        id: 1,
        question: "What are personal loan interest rates?",
        answer: "Personal loan interest rates range from 10.5% to 18% p.a. depending on credit score and bank. SBI: 10.5-16%, HDFC: 10.75-17%, ICICI: 11-17.5%, Axis: 11.25-18%.",
        emoji: "💰",
        category: "interest",
        keywords: ["interest", "rate", "personal loan", "percentage"]
    },
    {
        id: 2,
        question: "What are home loan interest rates?",
        answer: "Home loan interest rates range from 8.5% to 9.8% p.a. SBI: 8.5-9.5%, HDFC: 8.6-9.6%, ICICI: 8.7-9.7%, Axis: 8.8-9.8%. Women borrowers get 0.05% concession.",
        emoji: "🏠",
        category: "interest",
        keywords: ["interest", "rate", "home loan", "mortgage"]
    },
    {
        id: 3,
        question: "What are car loan interest rates?",
        answer: "Car loan interest rates range from 9.25% to 15% p.a. New cars: 9.25-13%, Used cars: 12-16%. EV vehicles get 0.5% concession.",
        emoji: "🚗",
        category: "interest",
        keywords: ["interest", "rate", "car loan", "auto loan"]
    },
    {
        id: 4,
        question: "What are education loan interest rates?",
        answer: "Education loan interest rates range from 11% to 16% p.a. India studies: 11-14%, Abroad studies: 12-16%. Merit scholarship: 1% off for 90%+.",
        emoji: "🎓",
        category: "interest",
        keywords: ["interest", "rate", "education loan", "student loan"]
    },
    {
        id: 5,
        question: "Eligibility for personal loan?",
        answer: "Personal loan eligibility: Age 21-60 years, Income ₹20,000+/month, Credit score 650+, Employment 1+ years. Self-employed need 2+ years business.",
        emoji: "✅",
        category: "eligibility",
        keywords: ["eligible", "eligibility", "personal loan", "qualify"]
    },
    {
        id: 6,
        question: "Eligibility for home loan?",
        answer: "Home loan eligibility: Age 21-65 years, Income ₹25,000+/month, Credit score 650+, Property value min ₹10 lakhs. Joint applicants get 40% higher eligibility.",
        emoji: "🏠",
        category: "eligibility",
        keywords: ["eligible", "eligibility", "home loan", "qualify"]
    },
    {
        id: 7,
        question: "Eligibility for car loan?",
        answer: "Car loan eligibility: Age 21-60 years, Income ₹15,000+/month, Credit score 600+. New cars: lower income accepted. Used cars: car age <5 years.",
        emoji: "🚗",
        category: "eligibility",
        keywords: ["eligible", "eligibility", "car loan", "qualify"]
    },
    {
        id: 8,
        question: "Eligibility for education loan?",
        answer: "Education loan eligibility: Student age 16-35 years, Admission to recognized course, Co-applicant income ₹25,000+/month. No collateral up to ₹4 lakhs.",
        emoji: "🎓",
        category: "eligibility",
        keywords: ["eligible", "eligibility", "education loan", "student"]
    },
    {
        id: 9,
        question: "What documents are needed for personal loan?",
        answer: "Personal loan documents: Identity proof (Aadhar/PAN), Address proof, Income proof (salary slips/IT returns), Bank statements (6 months), Passport photos.",
        emoji: "📄",
        category: "documents",
        keywords: ["document", "docs", "personal loan", "paperwork"]
    },
    {
        id: 10,
        question: "What documents are needed for home loan?",
        answer: "Home loan documents: Identity & address proof, Income proof, Property papers, Bank statements (12 months), IT returns (3 years), Processing fee cheque.",
        emoji: "🏠",
        category: "documents",
        keywords: ["document", "docs", "home loan", "property"]
    },
    {
        id: 11,
        question: "What documents are needed for car loan?",
        answer: "Car loan documents: Identity & address proof, Income proof, Bank statements (6 months), Car quotation, RC copy (used cars), Insurance, Photos.",
        emoji: "🚗",
        category: "documents",
        keywords: ["document", "docs", "car loan", "vehicle"]
    },
    {
        id: 12,
        question: "What documents are needed for education loan?",
        answer: "Education loan documents: Student ID, Admission letter, Fee structure, Marksheets, Co-applicant income proof, Bank statements, Collateral docs (if applicable).",
        emoji: "🎓",
        category: "documents",
        keywords: ["document", "docs", "education loan", "student"]
    },
    {
        id: 13,
        question: "What is the minimum credit score required?",
        answer: "Minimum credit score required: 650 for most loans. 750+ gets best interest rates. Credit score breakdown: 800+ Excellent, 750-799 Good, 700-749 Fair, 650-699 Poor, below 650 Bad.",
        emoji: "📊",
        category: "credit score",
        keywords: ["credit", "score", "cibil", "minimum"]
    },
    {
        id: 14,
        question: "What are the repayment options?",
        answer: "Repayment options: EMI (Monthly), Bullet payment, Step-up EMI, Step-down EMI, Prepayment allowed with nominal charges after 6 months.",
        emoji: "💳",
        category: "repayment",
        keywords: ["repayment", "pay", "emi", "monthly"]
    },
    {
        id: 15,
        question: "What are prepayment charges?",
        answer: "Prepayment charges: Floating rate loans - No charges. Fixed rate loans - 2-5% of outstanding amount. Usually allowed after 6-12 months.",
        emoji: "⏰",
        category: "prepayment",
        keywords: ["prepayment", "foreclosure", "charges", "penalty"]
    },
    {
        id: 16,
        question: "How long does loan approval usually take?",
        answer: "Approval time varies by bank but generally takes 1–3 business days after document submission.",
        emoji: "⏳",
        category: "process",
        keywords: ["approval", "time", "process"]
    },
    {
        id: 17,
        question: "Can I prepay only part of my loan?",
        answer: "Most lenders allow partial prepayment after six months with minimal charges; check your agreement.",
        emoji: "⚖️",
        category: "prepayment",
        keywords: ["partial", "prepayment", "foreclosure"]
    },
    {
        id: 18,
        question: "Is there a processing fee for loans?",
        answer: "Yes, processing fees typically range from 0.5% to 2% of the loan amount.",
        emoji: "📝",
        category: "charges",
        keywords: ["processing", "fee", "charges"]
    },
    {
        id: 19,
        question: "What is the maximum loan tenure?",
        answer: "Loan tenures can extend up to 30 years for home loans and 7 years for personal loans.",
        emoji: "📆",
        category: "terms",
        keywords: ["tenure", "maximum", "duration"]
    },
    {
        id: 20,
        question: "Do co-applicants improve eligibility?",
        answer: "Yes, having a co-applicant can increase eligibility and lower EMIs as incomes are combined.",
        emoji: "🤝",
        category: "eligibility",
        keywords: ["co-applicant", "joint", "eligibility"]
    },
    {
        id: 21,
        question: "Can self-employed individuals get loans?",
        answer: "Self-employed borrowers need 2+ years of business proof and higher income documents but are eligible.",
        emoji: "💼",
        category: "eligibility",
        keywords: ["self-employed", "business", "documents"]
    },
    {
        id: 22,
        question: "What happens if I miss an EMI?",
        answer: "Missing an EMI incurs a late fee (usually 1-2%) and affects your credit score.",
        emoji: "⚠️",
        category: "repayment",
        keywords: ["missed", "emi", "late fee"]
    },
    {
        id: 23,
        question: "Are interest rates fixed or floating?",
        answer: "Loans can have fixed rates (constant) or floating rates (linked to repo rate), affecting EMIs.",
        emoji: "🔁",
        category: "interest",
        keywords: ["fixed", "floating", "rate"]
    },
    {
        id: 24,
        question: "What is a balance transfer?",
        answer: "Balance transfer allows you to move your existing loan to another bank for a lower rate.",
        emoji: "🔄",
        category: "process",
        keywords: ["balance", "transfer", "switch"]
    },
    {
        id: 25,
        question: "Can I get a loan for property renovation?",
        answer: "Yes, some banks offer home improvement loans for renovation with lower rates.",
        emoji: "🛠️",
        category: "loan type",
        keywords: ["renovation", "property", "home improvement"]
    },
    {
        id: 26,
        question: "How is EMI calculated?",
        answer: "EMI = [P x r x (1+r)^n]/[(1+r)^n-1], where P=principal, r=monthly rate, n=number of months.",
        emoji: "🧮",
        category: "repayment",
        keywords: ["emi", "calculate", "formula"]
    },
    {
        id: 27,
        question: "Does CIBIL score matter for interest rate?",
        answer: "Yes, higher credit scores typically qualify for lower interest rates.",
        emoji: "📉",
        category: "credit score",
        keywords: ["cibil", "score", "rate"]
    },
    {
        id: 28,
        question: "Can I change my loan repayment date?",
        answer: "Some banks allow changing EMI date once or twice a year on request.",
        emoji: "📅",
        category: "repayment",
        keywords: ["change", "date", "emi"]
    },
    {
        id: 29,
        question: "Are there tax benefits on loan interest?",
        answer: "Yes, home loan interest is deductible under Section 24 and principal under 80C.",
        emoji: "🧾",
        category: "tax",
        keywords: ["tax", "benefit", "deduction"]
    },
    {
        id: 30,
        question: "What is foreclosure?",
        answer: "Foreclosure means paying off the entire loan before tenure ends; existing charges may apply.",
        emoji: "🏁",
        category: "prepayment",
        keywords: ["foreclosure", "repay", "early"]
    },
    {
        id: 31,
        question: "Can NRIs apply for loans?",
        answer: "Yes, NRIs can apply but need additional documents like NRI status proof and Indian address.",
        emoji: "🌍",
        category: "eligibility",
        keywords: ["NRI", "non resident", "loan"]
    },
    {
        id: 32,
        question: "Is loan insurance mandatory?",
        answer: "Loan insurance is optional but recommended to cover repayments in case of unforeseen events.",
        emoji: "🛡️",
        category: "insurance",
        keywords: ["insurance", "optional", "coverage"]
    },
    {
        id: 33,
        question: "What documents do salaried individuals need?",
        answer: "Salary slips (3 months), Form 16, bank statements (6 months), ID and address proof.",
        emoji: "📑",
        category: "documents",
        keywords: ["salary", "slips", "documents"]
    },
    {
        id: 34,
        question: "Can I pre-close a loan within 1 year?",
        answer: "Most banks allow pre-closure after 6-12 months with a small charge on fixed-rate loans.",
        emoji: "✅",
        category: "prepayment",
        keywords: ["pre-close", "early", "charge"]
    },
    {
        id: 35,
        question: "Do interest rates change during tenure?",
        answer: "Floating rates can change based on repo rate movements; fixed rates remain constant.",
        emoji: "🔄",
        category: "interest",
        keywords: ["change", "floating", "fixed"]
    },
    {
        id: 36,
        question: "What is a co-borrower?",
        answer: "A co-borrower is jointly responsible along with the primary borrower for repayment.",
        emoji: "👥",
        category: "eligibility",
        keywords: ["co-borrower", "joint", "loan"]
    },
    {
        id: 37,
        question: "How do I check loan application status?",
        answer: "Status can be checked online on the lender’s portal using your application ID.",
        emoji: "🔍",
        category: "process",
        keywords: ["status", "check", "application"]
    },
    {
        id: 38,
        question: "What is margin money?",
        answer: "Margin money is the borrower’s own contribution; banks finance the rest (typically 75-90%).",
        emoji: "💵",
        category: "loan terms",
        keywords: ["margin", "money", "contribution"]
    },
    {
        id: 39,
        question: "Can I apply for a top-up loan?",
        answer: "Top-up loans are available for existing borrowers with good repayment history.",
        emoji: "➕",
        category: "loan type",
        keywords: ["top-up", "additional", "loan"]
    },
    {
        id: 40,
        question: "What is the difference between secured and unsecured loan?",
        answer: "Secured loans require collateral; unsecured loans do not but have higher rates.",
        emoji: "🔐",
        category: "loan types",
        keywords: ["secured", "unsecured", "collateral"]
    },
    {
        id: 41,
        question: "How can I improve my credit score?",
        answer: "Pay EMIs on time, keep credit utilization low, and avoid multiple enquiries.",
        emoji: "📈",
        category: "credit score",
        keywords: ["improve", "score", "credit"]
    },
    {
        id: 42,
        question: "Does loan amount affect interest rate?",
        answer: "Larger loan amounts may attract slightly lower rates depending on the lender’s slabs.",
        emoji: "📊",
        category: "interest",
        keywords: ["amount", "rate", "slab"]
    },
    {
        id: 43,
        question: "Are there penalties for early prepayment?",
        answer: "Some banks charge 2-5% on outstanding for prepayment, mainly on fixed-rate loans.",
        emoji: "⚖️",
        category: "prepayment",
        keywords: ["penalty", "early", "charge"]
    },
    {
        id: 44,
        question: "What is an EMI calculator?",
        answer: "A tool that estimates monthly payments based on principal, rate and tenure.",
        emoji: "🧾",
        category: "repayment",
        keywords: ["calculator", "emi", "estimate"]
    },
    {
        id: 45,
        question: "Can I refinance my loan?",
        answer: "Refinancing replaces your loan with another at a better rate if available.",
        emoji: "♻️",
        category: "process",
        keywords: ["refinance", "replace", "rate"]
    },
    {
        id: 46,
        question: "What is the role of a guarantor?",
        answer: "A guarantor promises to repay the loan if the borrower defaults.",
        emoji: "👤",
        category: "process",
        keywords: ["guarantor", "security", "repay"]
    },
    {
        id: 47,
        question: "Can I change my loan EMI tenure mid-way?",
        answer: "Yes, some lenders permit tenure extension or reduction on request with documentation.",
        emoji: "🔁",
        category: "terms",
        keywords: ["change", "tenure", "mid-way"]
    },
    {
        id: 48,
        question: "Is there a penalty for cheque bounce?",
        answer: "Yes, banks charge a fee (₹100-₹500) if your EMI cheque bounces.",
        emoji: "📉",
        category: "charges",
        keywords: ["bounce", "cheque", "penalty"]
    },
    {
        id: 49,
        question: "Can I use loan for business expenses?",
        answer: "Personal and business loans have different criteria; use a business loan for expenses.",
        emoji: "🏢",
        category: "loan type",
        keywords: ["business", "expenses", "loan"]
    },
    {
        id: 50,
        question: "How do I track my loan repayment schedule?",
        answer: "Most banks provide an amortization table in statements or online portals.",
        emoji: "📅",
        category: "repayment",
        keywords: ["track", "schedule", "amortization"]
    }
];

// ============================================
// INITIALIZATION
// ============================================

// helper to load FAQ JSON and merge with built-in database
function loadFAQs() {
    const url = '../data/faq_data.json';
    return fetch(url)
        .then(res => {
            if (!res.ok) throw new Error('Network response was not ok');
            return res.json();
        })
        .then(data => {
            if (!Array.isArray(data)) throw new Error('Invalid FAQ JSON structure');
            // normalize each item to include keywords for consistent matching
            data.forEach(item => {
                if (!item.keywords) {
                    item.keywords = (item.tags || []).map(t => t.toLowerCase());
                }
            });
            // merge with built-in faqDatabase; avoid duplicates by question text
            const merged = faqDatabase.slice();
            const seen = new Set(merged.map(f => f.question.toLowerCase()));
            data.forEach(item => {
                if (!seen.has(item.question.toLowerCase())) {
                    merged.push(item);
                    seen.add(item.question.toLowerCase());
                }
            });
            return merged;
        });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing LoanFAQ Chatbot...');
    
    // Show AI page first (YOUR ORIGINAL LOGIC)
    document.getElementById('aiPage').style.display = 'block';
    document.getElementById('faqContainer').style.display = 'none';
    document.getElementById('minimizedAI').classList.add('hidden');
    document.getElementById('emiPage').classList.add('hidden');
    document.getElementById('eligibilityPage').classList.add('hidden');
    document.getElementById('loanSelectionPage').classList.add('hidden');
    
    // Set time-based greeting
    setTimeBasedGreeting();
    
    // Update current time
    updateCurrentTime();
    setInterval(updateCurrentTime, 60000);
    
    // Load FAQs either from external JSON or use built-in database
    loadFAQs()
        .then(faqs => {
            state.faqs = faqs;
            loadAllFAQs();
            updateCategoryCounts();
        })
        .catch(err => {
            console.error('Failed to load FAQs from JSON, falling back to built-in data', err);
            state.faqs = faqDatabase;
            loadAllFAQs();
            updateCategoryCounts();
        });
    
    // Update category counts (will also run after fetch above but safe fallback)
    // updateCategoryCounts();
    
    // Load saved theme
    loadSavedTheme();
    
    // Setup event listeners
    setupEventListeners();
    
    // Add welcome message to AI chat (YOUR ORIGINAL WELCOME MESSAGE)
    setTimeout(function() {
        addAIMessage("👋 Welcome! I'm Finova. Ask me about loans, interest rates, eligibility, documents, EMI, etc.");
    }, 500);
    
    console.log('✅ LoanFAQ initialized successfully!');
});

// ============================================
// TIME FUNCTIONS
// ============================================

function setTimeBasedGreeting() {
    const hour = new Date().getHours();
    let greeting;
    
    if (hour >= 5 && hour < 12) {
        greeting = "Good morning! ☀️ Welcome to LoanFAQ.";
    } else if (hour >= 12 && hour < 17) {
        greeting = "Good afternoon! 🌤️ Welcome to LoanFAQ.";
    } else if (hour >= 17 && hour < 21) {
        greeting = "Welcome to LoanFAQ.";
    } else {
        greeting = "Hello!  Welcome to LoanFAQ, feel free to ask anything.";
    }
    
    if (elements.timeGreeting) {
        elements.timeGreeting.textContent = greeting;
    }
}

function updateCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    
    if (elements.currentTime) {
        elements.currentTime.textContent = `${hours.toString().padStart(2, '0')}:${minutes} ${ampm}`;
    }
}

// ============================================
// AI PAGE FUNCTIONS - WITH BACKEND API (YOUR ORIGINAL LOGIC)
// ============================================

function minimizeAI() {
    document.getElementById('aiPage').style.display = 'none';
    document.getElementById('faqContainer').style.display = 'block';
    document.getElementById('minimizedAI').classList.remove('hidden');
}

function maximizeAI() {
    document.getElementById('minimizedAI').classList.add('hidden');
    document.getElementById('aiPage').style.display = 'block';
    document.getElementById('faqContainer').style.display = 'none';
}

// ========== YOUR ORIGINAL sendMessage WITH API CALL ==========
function sendMessage() {
    const input = document.getElementById('chatInput');
    if (!input) return;

    const message = input.value.trim();
    if (message === '') return;

    addMessage(message, 'user');
    input.value = '';

    showTypingIndicator();

    // 🔥 CALL BACKEND API (YOUR ORIGINAL CODE)
    fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator();
        addMessage(data.response, 'bot');
    })
    .catch(error => {
        removeTypingIndicator();
        // Fallback to local responses if API fails
        const localResponse = getLocalResponse(message);
        addMessage(localResponse, 'bot');
        console.error('Error:', error);
    });
}

// ========== YOUR ORIGINAL addMessage ==========
// helper that turns a raw text reply into a DOM node or nodes, applying
// simple bullet-point formatting when the message contains the • separator
function formatBotReply(text) {
    // if there are bullet markers we build a proper list
    if (text.includes('•')) {
        const parts = text.split('•').map(p => p.trim()).filter(p => p);
        const ul = document.createElement('ul');
        ul.className = 'bot-bullet-list';
        parts.forEach(part => {
            const li = document.createElement('li');
            li.textContent = part;
            ul.appendChild(li);
        });
        return ul;
    }
    // otherwise just return a text node
    return document.createTextNode(text);
}

function addMessage(text, sender) {
    const chatArea = document.getElementById('chatMessages');
    if (!chatArea) return;
    
    const messageRow = document.createElement('div');
    messageRow.className = 'message-row ' + sender;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble ' + sender;
    
    if (sender === 'bot') {
        // format bullet points or plain text
        const formatted = formatBotReply(text);
        bubble.appendChild(formatted);
    } else {
        bubble.textContent = text;
    }
    
    const time = document.createElement('div');
    time.className = 'message-time';
    const now = new Date();
    time.textContent = now.getHours().toString().padStart(2, '0') + ':' + 
                      now.getMinutes().toString().padStart(2, '0');
    
    messageRow.appendChild(bubble);
    messageRow.appendChild(time);
    chatArea.appendChild(messageRow);
    
    chatArea.scrollTop = chatArea.scrollHeight;
}

// simple wrapper used during initialization to show a welcome message in the AI chat
function addAIMessage(text) {
    // use the same renderer as addMessage, marking it as coming from the bot
    addMessage(text, 'bot');
}

// ========== YOUR ORIGINAL showTypingIndicator ==========
function showTypingIndicator() {
    const chatArea = document.getElementById('chatMessages');
    if (!chatArea) return;
    if (document.getElementById('typingIndicator')) return;
    
    const typingRow = document.createElement('div');
    typingRow.className = 'message-row bot';
    typingRow.id = 'typingIndicator';
    
    const typingBubble = document.createElement('div');
    typingBubble.className = 'message-bubble bot';
    typingBubble.innerHTML = '...';
    
    typingRow.appendChild(typingBubble);
    chatArea.appendChild(typingRow);
    chatArea.scrollTop = chatArea.scrollHeight;
}

// ========== YOUR ORIGINAL removeTypingIndicator ==========
function removeTypingIndicator() {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
}

// ========== YOUR ORIGINAL getResponse (Fallback) ==========
function getLocalResponse(message) {
    const lower = message.toLowerCase();
    
    if (lower.includes('hello') || lower.includes('hi')) {
        return "Hello! How can I help you with your loan today?";
    }
    if (lower.includes('interest') || lower.includes('rate')) {
        return "💰 Interest Rates:\n• Personal: 10.5% - 18%\n• Home: 8.5% - 9.8%\n• Car: 9.25% - 15%\n• Education: 11% - 16%";
    }
    if (lower.includes('eligibility')) {
        return "✅ Eligibility:\n• Age: 21-60 years\n• Income: ₹20,000+/month\n• Credit Score: 650+";
    }
    if (lower.includes('document')) {
        return "📄 Documents: Aadhar, PAN, Income proof, Bank statements, Photos";
    }
    if (lower.includes('credit') || lower.includes('score')) {
        return "📊 Credit Score:\n800+ Excellent\n750-799 Good\n700-749 Fair\n650-699 Poor\n<650 Bad";
    }
    if (lower.includes('emi')) {
        return "💳 Use our EMI calculator above for exact calculations!";
    }
    if (lower.includes('sbi')) {
        return "🏦 SBI: Personal 10.5%, Home 8.5%, Car 9.25%";
    }
    if (lower.includes('hdfc')) {
        return "🏦 HDFC: Personal 10.75%, Home 8.6%, Car 9.5%";
    }
    return "Ask me about interest rates, eligibility, documents, credit score, EMI, or specific banks like SBI, HDFC!";
}

// ============================================
// UPDATE CATEGORY COUNTS
// ============================================

function updateCategoryCounts() {
    // build count map from current faqs
    const counts = {};
    counts['all'] = state.faqs.length;
    state.faqs.forEach(faq => {
        const cat = faq.category.toLowerCase();
        counts[cat] = (counts[cat] || 0) + 1;
    });

    // update every sidebar category item using data-category attribute
    document.querySelectorAll('.category-item').forEach(item => {
        const cat = item.getAttribute('data-category');
        if (!cat) return;
        const span = item.querySelector('.count');
        if (span) {
            span.textContent = counts[cat.toLowerCase()] || 0;
        }
    });

    // Update total FAQs in header (reflect the actual number of loaded FAQs)
    const totalFAQsSpan = document.getElementById('totalFAQs');
    if (totalFAQsSpan) totalFAQsSpan.textContent = counts['all'] || 0;
}

// ============================================
// FAQ FUNCTIONS (YOUR ORIGINAL LOGIC)
// ============================================

function loadAllFAQs() {
    filterByCategory('all', document.querySelector('.category-item.active'));
}

function filterByCategory(category, element) {
    // Update active state
    document.querySelectorAll('.category-item').forEach(item => {
        item.classList.remove('active');
    });
    element.classList.add('active');
    
    state.activeCategory = category;
    
    // Filter FAQs
    let filteredFAQs = [];
    if (category === 'all') {
        filteredFAQs = state.faqs;
    } else {
        filteredFAQs = state.faqs.filter(faq => 
            faq.category.toLowerCase() === category.toLowerCase()
        );
    }
    
    // Update count
    if (elements.questionsCount) {
        elements.questionsCount.textContent = filteredFAQs.length;
    }
    
    // Render questions
    renderQuestions(filteredFAQs);
}

function renderQuestions(questions) {
    const container = document.getElementById('questionsList');
    if (!container) return;
    
    if (questions.length === 0) {
        container.innerHTML = `
            <div class="no-questions">
                <i class="fas fa-inbox"></i>
                <p>No questions found</p>
            </div>
        `;
        return;
    }
    
    // show up to 50 items initially, provide a way to show more
    const MAX_DISPLAY = 50;
    let html = '';
    const slice = questions.slice(0, MAX_DISPLAY);
    slice.forEach(q => {
        html += `
            <div class="question-card" onclick="askQuestion('${q.question.replace(/'/g, "\\'")}')">
                <i class="fas fa-question-circle"></i>
                <span>${q.question}</span>
            </div>
        `;
    });
    
    if (questions.length > MAX_DISPLAY) {
        html += `
            <div class="show-more-card" onclick="renderQuestions(questions)">
                <i class="fas fa-arrow-down"></i>
                <span>Show all ${questions.length} questions</span>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

function askQuestion(question) {
    const input = document.getElementById('messageInput');
    if (input) {
        input.value = question;
        sendChatMessage();
    }
}

function sendChatMessage() {
    const input = document.getElementById('messageInput');
    if (!input) return;

    const message = input.value.trim();
    if (message === '') return;

    addChatMessage(message, 'user');
    input.value = '';

    // quick local intention responses before showing typing
    let lower = message.toLowerCase();
    // normalize common shorthand/typos
    const normMap = {
        'gm': 'good morning',
        'gn': 'good night',
        'tq': 'thank you',
        'tnx': 'thanks',
        'thx': 'thanks',
        'sry': 'sorry',
        'evng': 'evening',
        'hlo': 'hello',
        'helo': 'hello'
    };
    Object.keys(normMap).forEach(k => {
        const re = new RegExp('\\b' + k + '\\b', 'g');
        lower = lower.replace(re, normMap[k]);
    });

    const greetings = ['hi','hello','hey','good morning','good afternoon','good evening','good night'];
    const thanks = ['thank', 'thanks', 'thank you', 'tq', 'tnx', 'thx'];
    const apologies = ['sorry', 'apology', 'apologies'];
    const farewells = ['bye','goodbye','see you','take care','good night','gn'];

    if (greetings.some(g => lower.startsWith(g))) {
        let reply = "Hello! How can I assist you today?";
        if (lower.startsWith('good morning')) {
            reply = "Good morning! How can I assist you today?";
        } else if (lower.startsWith('good afternoon')) {
            reply = "Good afternoon! How can I assist you today?";
        } else if (lower.startsWith('good evening')) {
            reply = "Good evening! How can I assist you today?";
        } else if (lower.startsWith('good night')) {
            reply = "Good night! Rest well and let me know if you have any loan questions.";
        }
        addChatMessage(reply, 'bot');
        return;
    }
    if (thanks.some(t => lower.includes(t))) {
        addChatMessage("You're welcome! 😊", 'bot');
        return;
    }
    if (apologies.some(a => lower.includes(a))) {
        addChatMessage("No worries! Let me know if you need any help.", 'bot');
        return;
    }
    if (farewells.some(f => lower.includes(f))) {
        addChatMessage("Goodbye! Feel free to come back anytime.", 'bot');
        return;
    }

    showTyping();

    setTimeout(() => {
        hideTyping();
        
        // Find matching FAQ
        const matchedFAQ = findMatchingFAQ(message);
        
        if (matchedFAQ) {
            addChatMessage(matchedFAQ.answer, 'bot');
        } else {
            addChatMessage("I don't have that specific answer. Please use the AI assistant for further help.", 'bot');
        }
    }, 1000);
}

function findMatchingFAQ(message) {
    let lower = message.toLowerCase().trim();
    // normalize same shortcuts as chat input
    const normMap = {
        'gm': 'good morning',
        'gn': 'good night',
        'tq': 'thank you',
        'tnx': 'thanks',
        'thx': 'thanks',
        'sry': 'sorry',
        'evng': 'evening',
        'hlo': 'hello',
        'helo': 'hello'
    };
    Object.keys(normMap).forEach(k => {
        const re = new RegExp('\\b' + k + '\\b', 'g');
        lower = lower.replace(re, normMap[k]);
    });

    // ignore very short queries or just greetings so they don't match substrings
    if (lower.length < 3) return null;
    const greetings = ['hi','hello','hey','good morning','good afternoon','good evening','good night'];
    for (const g of greetings) {
        if (lower === g || lower.startsWith(g + ' ') || lower.endsWith(' ' + g)) {
            return null;
        }
    }

    // Try exact match or whole-word containment to prevent substring collisions
    const exactMatch = state.faqs.find(faq => {
        const q = faq.question.toLowerCase();
        if (q === lower) return true;
        // word boundary check: look for ' lower ' inside q or vice versa
        if ((' ' + q + ' ').includes(' ' + lower + ' ')) return true;
        if ((' ' + lower + ' ').includes(' ' + q + ' ')) return true;
        return false;
    });
    
    if (exactMatch) return exactMatch;
    
    // Try keyword/tags matches
    const keywordMatch = state.faqs.find(faq => {
        const kws = (faq.keywords || []).map(k => k.toLowerCase());
        // also include tags if present
        if (faq.tags) kws.push(...faq.tags.map(t => t.toLowerCase()));
        return kws.some(keyword => lower.includes(keyword));
    });
    
    if (keywordMatch) return keywordMatch;
    
    // attempt basic similarity by requiring at least two "meaningful" words match
    const messageWords = (lower.match(/\b\w+\b/g) || []).filter(w => w.length > 3);
    if (messageWords.length >= 2) {
        const simMatch = state.faqs.find(faq => {
            const q = faq.question.toLowerCase();
            // count how many of the message words appear in the question
            let hits = 0;
            messageWords.forEach(w => {
                if (q.includes(w)) hits++;
            });
            return hits >= 2; // require at least two words
        });
        if (simMatch) return simMatch;
    }
    
    return null;
}

function addChatMessage(text, sender) {
    const container = document.getElementById('messagesContainer');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const time = new Date().toLocaleTimeString([], { 
        hour: '2-digit', minute: '2-digit' 
    });
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">
                <p>${text.replace(/\n/g, '<br>')}</p>
            </div>
            <div class="message-footer">
                <span class="time">${time}</span>
            </div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    state.isTyping = true;
    if (elements.typingIndicator) {
        elements.typingIndicator.classList.remove('hidden');
    }
}

function hideTyping() {
    state.isTyping = false;
    if (elements.typingIndicator) {
        elements.typingIndicator.classList.add('hidden');
    }
}

function searchFAQ() {
    const searchTerm = document.getElementById('faqSearch').value.toLowerCase().trim();
    
    if (searchTerm === '') {
        filterByCategory(state.activeCategory, document.querySelector('.category-item.active'));
        return;
    }
    
    const results = state.faqs.filter(faq => {
        if (faq.question.toLowerCase().includes(searchTerm)) return true;
        if (faq.answer.toLowerCase().includes(searchTerm)) return true;
        if (faq.keywords.some(keyword => keyword.includes(searchTerm))) return true;
        return false;
    });
    
    if (elements.questionsCount) {
        elements.questionsCount.textContent = results.length;
    }
    
    renderQuestions(results);
}

function quickQuestion(question) {
    const input = document.getElementById('messageInput');
    if (input) {
        input.value = question;
        sendChatMessage();
    }
}

function clearChat() {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = `
        <div class="message bot">
            <div class="message-content">
                <div class="message-text">
                    <p>👋 Hello! I'm here to help with your loan questions. Ask anything about loans, interest rates, eligibility, or documents.</p>
                </div>
                <div class="message-footer">
                    <span class="time">Just now</span>
                </div>
            </div>
        </div>
    `;
}

// ============================================
// NAVIGATION FUNCTIONS (YOUR ORIGINAL LOGIC)
// ============================================

function navigateTo(page) {
    console.log('Navigate to:', page);
    
    document.getElementById('faqContainer').style.display = 'none';
    document.getElementById('emiPage').classList.add('hidden');
    document.getElementById('eligibilityPage').classList.add('hidden');
    document.getElementById('loanSelectionPage').classList.add('hidden');
    
    // ADD THIS LINE - Hide Ask Finova button
    document.getElementById('minimizedAI').style.display = 'none';
    
    if (page === 'emi') {
        document.getElementById('emiPage').classList.remove('hidden');
        resetEMICalculator();
    } else if (page === 'eligibility') {
        document.getElementById('eligibilityPage').classList.remove('hidden');
        resetEligibilityChecker();
    }
}

function goBack() {
    console.log('Going back to FAQ');
    
    resetEMICalculator();
    resetEligibilityChecker();
    
    document.getElementById('faqContainer').style.display = 'block';
    document.getElementById('emiPage').classList.add('hidden');
    document.getElementById('eligibilityPage').classList.add('hidden');
    document.getElementById('loanSelectionPage').classList.add('hidden');
    
    // ADD THIS LINE - Show Ask Finova button again on FAQ page
    document.getElementById('minimizedAI').style.display = 'flex';
}

// ============================================
// EMI CALCULATOR FUNCTIONS (YOUR ORIGINAL LOGIC)
// ============================================

function resetEMICalculator() {
    document.getElementById('emiLoanAmount').value = 500000;
    document.getElementById('emiInterestRate').value = 10.5;
    document.getElementById('emiTenure').value = 5;
    document.getElementById('emiCreditScore').value = 750;
    
    document.getElementById('emiResult').classList.add('hidden');
    document.getElementById('missedPaymentResult').classList.add('hidden');
    
    removeLoanIndicator();
    state.currentLoanType = 'none';
}

function resetEligibilityChecker() {
    document.getElementById('eligibilityIncome').value = 50000;
    document.getElementById('eligibilityAge').value = 30;
    document.getElementById('eligibilityCreditScore').value = 750;
    document.getElementById('eligibilityExistingEmi').value = 0;
    document.getElementById('eligibilityResult').innerHTML = '';
}

function showLoanSelection() {
    document.getElementById('emiPage').classList.add('hidden');
    document.getElementById('loanSelectionPage').classList.remove('hidden');
}

function hideLoanSelection() {
    document.getElementById('loanSelectionPage').classList.add('hidden');
    document.getElementById('emiPage').classList.remove('hidden');
}

function selectLoanAndCalculate(type) {
    state.currentLoanType = type;
    
    if (type === 'personal') {
        document.getElementById('emiLoanAmount').value = 500000;
        document.getElementById('emiInterestRate').value = 10.5;
    } else if (type === 'home') {
        document.getElementById('emiLoanAmount').value = 5000000;
        document.getElementById('emiInterestRate').value = 8.5;
    } else if (type === 'car') {
        document.getElementById('emiLoanAmount').value = 500000;
        document.getElementById('emiInterestRate').value = 9.5;
    } else if (type === 'education') {
        document.getElementById('emiLoanAmount').value = 500000;
        document.getElementById('emiInterestRate').value = 11.0;
    }
    
    removeLoanIndicator();
    addLoanIndicator(type);
    
    document.getElementById('emiResult').classList.add('hidden');
    document.getElementById('missedPaymentResult').classList.add('hidden');
    
    hideLoanSelection();
}

function addLoanIndicator(type) {
    const calculatorContent = document.querySelector('.calculator-content');
    if (!calculatorContent) return;
    
    removeLoanIndicator();
    
    const indicator = document.createElement('div');
    indicator.id = 'loanIndicator';
    indicator.className = 'loan-indicator';
    
    let icon = '', name = '';
    
    if (type === 'personal') {
        icon = 'fa-user';
        name = 'Personal Loan';
    } else if (type === 'home') {
        icon = 'fa-home';
        name = 'Home Loan';
    } else if (type === 'car') {
        icon = 'fa-car';
        name = 'Car Loan';
    } else if (type === 'education') {
        icon = 'fa-graduation-cap';
        name = 'Education Loan';
    }
    
    indicator.innerHTML = `
        <div class="loan-indicator-content">
            <i class="fas ${icon}"></i>
            <span><strong>Selected:</strong> ${name}</span>
            <button onclick="clearLoanSelection()" class="clear-loan-btn">
                <i class="fas fa-times"></i> Clear
            </button>
        </div>
    `;
    
    calculatorContent.insertBefore(indicator, calculatorContent.firstChild);
}

function removeLoanIndicator() {
    const indicator = document.getElementById('loanIndicator');
    if (indicator) indicator.remove();
}

function clearLoanSelection() {
    state.currentLoanType = 'none';
    removeLoanIndicator();
    
    document.getElementById('emiLoanAmount').value = 500000;
    document.getElementById('emiInterestRate').value = 10.5;
    document.getElementById('emiTenure').value = 5;
    
    calculateEMI();
}

function calculateEMI() {
    const amount = parseFloat(document.getElementById('emiLoanAmount').value) || 0;
    const rate = parseFloat(document.getElementById('emiInterestRate').value) || 0;
    const years = parseFloat(document.getElementById('emiTenure').value) || 0;
    const creditScore = parseInt(document.getElementById('emiCreditScore').value) || 0;
    
    if (amount <= 0) {
        alert('Please enter loan amount');
        return;
    }
    if (rate <= 0) {
        alert('Please enter interest rate');
        return;
    }
    if (years <= 0) {
        alert('Please enter tenure');
        return;
    }
    if (creditScore < 300 || creditScore > 900) {
        alert('Please enter valid credit score (300-900)');
        return;
    }
    
    const months = years * 12;
    const monthlyRate = rate / (12 * 100);
    const emi = amount * monthlyRate * Math.pow(1 + monthlyRate, months) / (Math.pow(1 + monthlyRate, months) - 1);
    
    if (isFinite(emi)) {
        document.getElementById('emiResult').classList.remove('hidden');
        document.getElementById('emiAmount').textContent = '₹' + Math.round(emi).toLocaleString();
        document.getElementById('totalInterest').textContent = '₹' + Math.round(emi * months - amount).toLocaleString();
        document.getElementById('totalPayment').textContent = '₹' + Math.round(emi * months).toLocaleString();
    }
}

function calculateMissedPayment() {
    const emiAmount = document.getElementById('emiAmount').textContent.replace('₹', '').replace(/,/g, '');
    if (emiAmount && emiAmount !== '₹0' && emiAmount !== '0') {
        document.getElementById('missedPaymentResult').classList.remove('hidden');
        const emi = parseFloat(emiAmount);
        const months = parseInt(document.getElementById('missedMonths').value) || 1;
        const penalty = emi * 0.02 * months;
        const nextPayment = emi + penalty;
        document.getElementById('nextMonthAmount').textContent = '₹' + Math.round(nextPayment).toLocaleString();
    } else {
        alert('Please calculate EMI first');
    }
}

// ============================================
// ELIGIBILITY CHECKER FUNCTIONS (YOUR ORIGINAL LOGIC)
// ============================================

function checkEligibility() {
    const income = parseFloat(document.getElementById('eligibilityIncome').value) || 0;
    const age = parseInt(document.getElementById('eligibilityAge').value) || 0;
    const creditScore = parseInt(document.getElementById('eligibilityCreditScore').value) || 0;
    const existingEmi = parseFloat(document.getElementById('eligibilityExistingEmi').value) || 0;
    
    const resultDiv = document.getElementById('eligibilityResult');
    
    const annualIncome = income * 12;
    
    let eligibilityPercentage = 0, maxLoanAmount = 0, interestRate = 0;
    let category = '', color = '', message = '';
    
    if (creditScore >= 800) {
        category = 'Excellent';
        eligibilityPercentage = 0.60;
        interestRate = 8.5;
        color = '#10b981';
        message = '✅ You are ELIGIBLE for best rates!';
    } 
    else if (creditScore >= 750) {
        category = 'Good';
        eligibilityPercentage = 0.50;
        interestRate = 10.5;
        color = '#10b981';
        message = '✅ You are ELIGIBLE!';
    }
    else if (creditScore >= 700) {
        category = 'Fair';
        eligibilityPercentage = 0.40;
        interestRate = 12.5;
        color = '#f59e0b';
        message = '⚠️ Moderate Eligibility';
    }
    else if (creditScore >= 650) {
        category = 'Average';
        eligibilityPercentage = 0.25;
        interestRate = 14.5;
        color = '#f59e0b';
        message = '⚠️ Limited Eligibility';
    }
    else if (creditScore >= 600) {
        category = 'Poor';
        eligibilityPercentage = 0.15;
        interestRate = 16.5;
        color = '#ef4444';
        message = '❌ Very Limited Eligibility';
    }
    else {
        category = 'Bad';
        eligibilityPercentage = 0;
        interestRate = 0;
        color = '#ef4444';
        message = '❌ Not Eligible';
    }
    
    maxLoanAmount = annualIncome * eligibilityPercentage;
    
    const monthlyMultiplier = {
        'Excellent': 30, 'Good': 24, 'Fair': 18, 'Average': 12, 'Poor': 8, 'Bad': 0
    };
    
    const maxByMultiplier = income * (monthlyMultiplier[category] || 0);
    
    if (maxByMultiplier > 0 && maxByMultiplier < maxLoanAmount) {
        maxLoanAmount = maxByMultiplier;
    }
    
    if (existingEmi > 0) {
        maxLoanAmount = Math.max(0, maxLoanAmount - (existingEmi * 36));
    }
    
    let issues = [];
    if (age < 21) issues.push('Minimum age required: 21 years');
    else if (age > 60) issues.push('Maximum age allowed: 60 years (65 for home loans)');
    if (income < 15000) issues.push('Minimum monthly income: ₹15,000');
    if (creditScore < 600) issues.push('Credit score below 600 - Not eligible for most loans');
    if (existingEmi > income * 0.5) issues.push('Existing EMIs exceed 50% of your income');
    
    let formattedAmount = '';
    if (maxLoanAmount >= 10000000) {
        formattedAmount = '₹' + (maxLoanAmount / 10000000).toFixed(2) + ' Crore';
    } else if (maxLoanAmount >= 100000) {
        formattedAmount = '₹' + (maxLoanAmount / 100000).toFixed(2) + ' Lakh';
    } else {
        formattedAmount = '₹' + maxLoanAmount.toLocaleString();
    }
    
    if (creditScore < 600 || issues.length > 0) {
        let issuesHtml = issues.map(issue => `<li style="color: ${color}; margin-bottom: 8px;">❌ ${issue}</li>`).join('');
        
        resultDiv.innerHTML = `
            <div style="border: 3px solid ${color}; border-radius: 15px; padding: 20px; margin-top: 20px;">
                <h2 style="color: ${color};">${message}</h2>
                <p style="margin: 10px 0;">Credit Score: <strong>${creditScore} (${category})</strong></p>
                <div style="text-align: left; margin-top: 15px;">
                    <h4 style="margin-bottom: 10px;">Issues to resolve:</h4>
                    <ul style="list-style: none; padding: 0;">
                        ${issuesHtml}
                    </ul>
                </div>
            </div>
        `;
    } else {
        resultDiv.innerHTML = `
            <div style="border: 3px solid ${color}; border-radius: 15px; padding: 25px; margin-top: 20px;">
                <h2 style="color: ${color};">${message}</h2>
                <div style="background: ${color}10; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="font-size: 14px; color: #666;">Your Credit Score</p>
                    <p style="font-size: 24px; font-weight: bold; color: ${color};">${creditScore} <span style="font-size: 16px;">(${category})</span></p>
                </div>
                <div style="margin: 20px 0;">
                    <p style="font-size: 14px; color: #666;">Maximum Loan Amount You Can Get</p>
                    <p style="font-size: 36px; font-weight: bold; color: ${color};">${formattedAmount}</p>
                </div>
            </div>
        `;
    }
}

// ============================================
// THEME FUNCTIONS
// ============================================

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    // Update icon
    const icon = document.querySelector('#themeToggle i');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
    
    // Save preference
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        const icon = document.querySelector('#themeToggle i');
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    }
});

function loadSavedTheme() {
    const savedTheme = localStorage.getItem('loanfaq-theme');
    if (savedTheme === 'dark') {
        state.isDarkMode = true;
        document.body.classList.add('dark-theme');
        const icon = document.querySelector('#themeToggle i');
        if (icon) icon.className = 'fas fa-sun';
    }
}

// ============================================
// EVENT LISTENERS
// ============================================

function setupEventListeners() {
    // Enter key for main chat
    if (elements.messageInput) {
        elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    
    // Enter key for AI chat (YOUR ORIGINAL)
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && document.activeElement === document.getElementById('chatInput')) {
            sendMessage();
        }
    });
    
    // Search functionality
    if (elements.faqSearch) {
        elements.faqSearch.addEventListener('input', searchFAQ);
    }
}

// ============================================
// BANK THEMED ANIME EFFECTS (YOUR ORIGINAL)
// ============================================

// Create floating coins
function createCoin() {
    const coin = document.createElement('div');
    coin.className = 'coin';
    coin.style.left = Math.random() * 100 + '%';
    coin.style.animationDuration = (Math.random() * 5 + 5) + 's';
    coin.style.width = (Math.random() * 20 + 15) + 'px';
    coin.style.height = coin.style.width;
    document.body.appendChild(coin);
    
    setTimeout(() => {
        coin.remove();
    }, 10000);
}

// Create coins every 3 seconds
setInterval(createCoin, 3000);

// Create bank-themed sparkles on click
document.addEventListener('click', function(e) {
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const sparkle = document.createElement('div');
            sparkle.className = 'bank-sparkle';
            sparkle.style.left = (e.pageX - 3 + (Math.random() * 20 - 10)) + 'px';
            sparkle.style.top = (e.pageY - 3 + (Math.random() * 20 - 10)) + 'px';
            document.body.appendChild(sparkle);
            
            setTimeout(() => {
                sparkle.remove();
            }, 1000);
        }, i * 100);
    }
});

// Add bank silhouette
const bankSilhouette = document.createElement('div');
bankSilhouette.className = 'bank-silhouette';
document.body.appendChild(bankSilhouette);




// ============================================
// MAKE FUNCTIONS GLOBAL
// ============================================

window.minimizeAI = minimizeAI;
window.maximizeAI = maximizeAI;
window.sendMessage = sendMessage;
window.sendChatMessage = sendChatMessage;
window.filterByCategory = filterByCategory;
window.quickQuestion = quickQuestion;
window.navigateTo = navigateTo;
window.goBack = goBack;
window.toggleDarkMode = toggleDarkMode;
window.calculateEMI = calculateEMI;
window.calculateMissedPayment = calculateMissedPayment;
window.showLoanSelection = showLoanSelection;
window.hideLoanSelection = hideLoanSelection;
window.selectLoanAndCalculate = selectLoanAndCalculate;
window.clearLoanSelection = clearLoanSelection;
window.checkEligibility = checkEligibility;
window.askQuestion = askQuestion;
window.searchFAQ = searchFAQ;
window.clearChat = clearChat;
window.resetEMICalculator = resetEMICalculator;
window.resetEligibilityChecker = resetEligibilityChecker;

// Force hide Ask Finova button on EMI and Eligibility pages
function forceHideAskFinova() {
    const askFinovaBtn = document.getElementById('minimizedAI');
    const emiPage = document.getElementById('emiPage');
    const eligibilityPage = document.getElementById('eligibilityPage');
    
    // Check every second if we're on EMI or Eligibility page
    setInterval(function() {
        // If EMI page is visible OR Eligibility page is visible
        if (!emiPage.classList.contains('hidden') || !eligibilityPage.classList.contains('hidden')) {
            askFinovaBtn.style.display = 'none';
            askFinovaBtn.classList.add('hidden');
        } else {
            // Only show on FAQ page if AI is minimized
            const aiPage = document.getElementById('aiPage');
            if (aiPage.style.display !== 'block') {
                askFinovaBtn.style.display = 'flex';
                askFinovaBtn.classList.remove('hidden');
            }
        }
    }, 100); // Check every 100ms (very fast)
}

// Run it when page loads
document.addEventListener('DOMContentLoaded', function() {
    forceHideAskFinova();
});

// Add this at the beginning of your file
function showAskFinovaOnFAQ() {
    const askBtn = document.getElementById('minimizedAI');
    const aiPage = document.getElementById('aiPage');
    const emiPage = document.getElementById('emiPage');
    const eligibilityPage = document.getElementById('eligibilityPage');
    
    // Only show on FAQ page when AI is minimized
    if (aiPage.style.display !== 'block' && 
        emiPage.classList.contains('hidden') && 
        eligibilityPage.classList.contains('hidden')) {
        askBtn.style.display = 'flex';
    } else {
        askBtn.style.display = 'none';
    }
}

// Call this function whenever page changes
setInterval(showAskFinovaOnFAQ, 500);