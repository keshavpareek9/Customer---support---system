from simple_agents import SimpleClassifierAgent, SimpleResponseAgent, SimpleReviewAgent

class CustomerSupportSystem:
    def __init__(self, use_simple=True):
        if use_simple:
            self.classifier = SimpleClassifierAgent()
            self.response_agent = SimpleResponseAgent()
            self.review_agent = SimpleReviewAgent()
        else:
            # Fallback to the Hugging Face version if needed
            from agents.classifier_agent import ClassifierAgent
            from agents.response_agent import ResponseAgent
            from agents.review_agent import ReviewAgent
            
            self.classifier = ClassifierAgent()
            self.response_agent = ResponseAgent()
            self.review_agent = ReviewAgent()
    
    def process_query(self, query):
        print("Classifying query...")
        category = self.classifier.classify_query(query)
        print(f"Category: {category}")
        
        print("Drafting response...")
        draft_response = self.response_agent.generate_response(query, category)
        print(f"Draft response: {draft_response}")
        
        print("Reviewing response...")
        final_response = self.review_agent.review_response(query, category, draft_response)
        print(f"Final response: {final_response}")
        
        return {
            "category": category,
            "response": final_response
        }

# For testing
if __name__ == "__main__":
    support_system = CustomerSupportSystem(use_simple=True)
    
    # Test queries
    test_queries = [
        "How can I change my credit card information?",
        "The app keeps crashing when I open it",
        "What are your operating hours?",
        "I need help with my password"
    ]
    
    for i, test_query in enumerate(test_queries):
        print(f"\n{'='*50}")
        print(f"Test {i+1}: {test_query}")
        print(f"{'='*50}")
        result = support_system.process_query(test_query)
        print(f"Category: {result['category']}")
        print(f"Response: {result['response']}")