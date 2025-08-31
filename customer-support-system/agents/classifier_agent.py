from transformers import pipeline
import re

class ClassifierAgent:
    def __init__(self):
        # Use a smaller, faster model for classification
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1  # Use CPU (-1) instead of GPU (0)
        )
    
    def classify_query(self, query):
        try:
            # Define our categories
            candidate_labels = ["billing", "technical", "general"]
            
            # Classify the query
            result = self.classifier(
                query,
                candidate_labels,
                hypothesis_template="This text is about {}."
            )
            
            # Return the label with the highest score
            return result['labels'][0]
        except Exception as e:
            print(f"Error in classification: {e}")
            return "general"  # Fallback category