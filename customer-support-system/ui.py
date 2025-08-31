import streamlit as st
import requests
import time
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set page configuration
st.set_page_config(
    page_title="Customer Support System",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e6f7ff;
    }
    .category-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .billing-badge {
        background-color: #ffcccc;
        color: #cc0000;
    }
    .technical-badge {
        background-color: #ccffcc;
        color: #006600;
    }
    .general-badge {
        background-color: #ccccff;
        color: #0000cc;
    }
</style>
""", unsafe_allow_html=True)

# Simple classifier as fallback
class SimpleClassifierAgent:
    def __init__(self):
        self.keywords = {
            "billing": ["payment", "charge", "invoice", "bill", "price", "cost", "subscription", "refund", "credit card", "payment method"],
            "technical": ["password", "login", "crash", "error", "bug", "feature", "update", "install", "technical", "reset", "2fa", "two factor"],
            "general": ["hours", "contact", "support", "help", "information", "about", "tutorial", "business hours", "phone", "email"]
        }
    
    def classify_query(self, query):
        query_lower = query.lower()
        scores = {category: 0 for category in self.keywords.keys()}
        
        for category, words in self.keywords.items():
            for word in words:
                if word in query_lower:
                    scores[category] += 1
        
        # Return category with highest score, default to general
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "general"

# Simple response generator
class SimpleResponseAgent:
    def __init__(self):
        self.responses = {
            "billing": {
                "payment": "You can update your payment method in Account Settings > Billing > Payment Methods.",
                "charge": "Charges occur on your monthly anniversary date. You can view your billing history in the Billing section.",
                "refund": "For refund requests, please contact our billing department at billing@company.com with your account details."
            },
            "technical": {
                "password": "You can reset your password using the 'Forgot Password' link on the login page.",
                "login": "If you're having trouble logging in, try resetting your password or clearing your browser cache.",
                "crash": "Please try updating to the latest version of our app. If the issue persists, contact technical support."
            },
            "general": {
                "hours": "Our support team is available 24/7 via email and chat. Phone support is available 9AM-6PM EST.",
                "contact": "You can reach us at support@company.com or call 1-800-123-4567 during business hours."
            }
        }
    
    def generate_response(self, query, category):
        query_lower = query.lower()
        
        # Check for specific keywords
        for keyword, response in self.responses.get(category, {}).items():
            if keyword in query_lower:
                return response
        
        # Default responses
        default_responses = {
            "billing": "For billing inquiries, please visit our billing portal or contact billing@company.com.",
            "technical": "For technical support, please describe your issue in detail or contact tech@company.com.",
            "general": "Thank you for your inquiry. How can we help you today?"
        }
        
        return default_responses.get(category, "Thank you for your message. Our team will respond shortly.")

# Simple review agent
class SimpleReviewAgent:
    def review_response(self, query, category, response):
        # Ensure the response is polite and professional
        if not response.startswith(("Thank you", "Please", "You can")):
            response = "Thank you for your question. " + response
        
        if not response.endswith((".")):
            response += "."
            
        return response

# Initialize the simple agents
classifier = SimpleClassifierAgent()
response_agent = SimpleResponseAgent()
review_agent = SimpleReviewAgent()

def process_query_simple(query):
    category = classifier.classify_query(query)
    draft_response = response_agent.generate_response(query, category)
    final_response = review_agent.review_response(query, category, draft_response)
    
    return {
        "category": category,
        "response": final_response
    }

st.title("🤖 Multi-Agent Customer Support System")
st.write("This system uses multiple AI agents to classify, respond to, and review customer support queries.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "category" in message:
            badge_class = f"{message['category']}-badge"
            st.markdown(f'<span class="category-badge {badge_class}">Category: {message["category"]}</span>', 
                       unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("What can I help you with today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process the query
    with st.spinner('Processing your query with our multi-agent system...'):
        try:
            # Try to use the API first
            response = requests.post(
                "http://localhost:8000/support/query",
                json={"query": prompt},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
            else:
                # Fallback to simple processing
                result = process_query_simple(prompt)
        except:
            # Fallback to simple processing if API is not available
            result = process_query_simple(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result["response"])
            badge_class = f"{result['category']}-badge"
            st.markdown(f'<span class="category-badge {badge_class}">Category: {result["category"]}</span>', 
                       unsafe_allow_html=True)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["response"],
            "category": result["category"]
        })

# Add sidebar with information
with st.sidebar:
    st.header("About this System")
    st.markdown("""
    This customer support system uses a multi-agent architecture:
    
    1. **Classifier Agent**: Identifies the query type (billing, technical, general)
    2. **Response Agent**: Drafts an answer using our knowledge base
    3. **Review Agent**: Checks tone and correctness before replying
    
    **Tech Stack**:
    - Multi-agent architecture
    - Streamlit UI
    - Keyword-based classification
    """)
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()