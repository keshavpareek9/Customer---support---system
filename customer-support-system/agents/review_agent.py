from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import pipeline

class ReviewAgent:
    def __init__(self):
        # Use a smaller model for review
        review_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            device=-1,  # Use CPU
            max_length=300
        )
        self.llm = HuggingFacePipeline(pipeline=review_pipeline)
    
    def review_response(self, query, category, response):
        try:
            prompt = PromptTemplate(
                input_variables=["query", "category", "response"],
                template="Review this customer support response. Check for tone and correctness. Query: {query}. Category: {category}. Response: {response}. Improved response:"
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            return chain.run(query=query, category=category, response=response)
        except Exception as e:
            print(f"Error in review: {e}")
            return response  # Return the original response if review fails