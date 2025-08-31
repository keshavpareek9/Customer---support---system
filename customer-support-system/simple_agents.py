import json
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np

class SimpleClassifierAgent:
    def __init__(self):
        self.keywords = {
            "billing": ["payment", "charge", "invoice", "bill", "price", "cost", "subscription", "refund"],
            "technical": ["password", "login", "crash", "error", "bug", "feature", "update", "install", "technical"],
            "general": ["hours", "contact", "support", "help", "information", "about"]
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

class SimpleResponseAgent:
    def __init__(self):
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self.load_knowledge_base()
    
    def load_knowledge_base(self):
        with open('knowledge_base/faq.json', 'r') as f:
            return json.load(f)
    
    def generate_response(self, query, category):
        try:
            # Get FAQs for the category
            faqs = self.knowledge_base.get(category, [])
            
            if not faqs:
                return "I don't have information on that topic. Please contact our support team."
            
            # Find the most similar question
            questions = [qa['question'] for qa in faqs]
            question_embeddings = self.embeddings.encode(questions)
            query_embedding = self.embeddings.encode([query])
            
            # Calculate similarity
            similarities = util.cos_sim(query_embedding, question_embeddings)[0]
            most_similar_idx = np.argmax(similarities)
            
            # Return the answer if similarity is high enough
            if similarities[most_similar_idx] > 0.3:
                return faqs[most_similar_idx]['answer']
            else:
                return f"I'm not sure about that specific question. For {category} issues, you can contact our support team."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm experiencing technical difficulties."

class SimpleReviewAgent:
    def __init__(self):
        self.positive_phrases = ["thank you", "please", "apologize", "sorry", "happy to help", "assist", "support"]
        self.negative_phrases = ["idiot", "stupid", "hate", "worthless", "useless", "terrible"]
    
    def review_response(self, query, category, response):
        # Simple tone check - just make sure it doesn't contain negative phrases
        response_lower = response.lower()
        
        for phrase in self.negative_phrases:
            if phrase in response_lower:
                response = response.replace(phrase, "[redacted]")
        
        # Ensure it has a professional closing
        if not any(phrase in response_lower for phrase in ["thank you", "please", "contact support"]):
            response += " Please contact our support team if you need further assistance."
        
        return response