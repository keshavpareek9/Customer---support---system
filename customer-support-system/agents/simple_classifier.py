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