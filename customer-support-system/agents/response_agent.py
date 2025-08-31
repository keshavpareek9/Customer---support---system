from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import json
import torch

class ResponseAgent:
    def __init__(self):
        # Setup a local LLM for response generation
        model_name = "microsoft/DialoGPT-medium"  # Smaller model that can run on CPU
        
        # Initialize the text generation pipeline
        self.llm = self.setup_local_llm(model_name)
        self.embeddings = HuggingFaceEmbeddings()
        self.vectorstore = self.setup_knowledge_base()
    
    def setup_local_llm(self, model_name):
        try:
            # Use a smaller model that can run on CPU
            text_gen_pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                device=-1,  # Use CPU
                max_length=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=50256  # Specific to GPT models
            )
            
            return HuggingFacePipeline(pipeline=text_gen_pipeline)
        except Exception as e:
            print(f"Error setting up local LLM: {e}")
            return None
    
    def setup_knowledge_base(self):
        try:
            # Load FAQ knowledge base
            with open('knowledge_base/faq.json', 'r') as f:
                faq_data = json.load(f)
            
            # Create documents for vector store
            documents = []
            for category, qa_pairs in faq_data.items():
                for qa in qa_pairs:
                    doc_text = f"Category: {category}. Question: {qa['question']}. Answer: {qa['answer']}"
                    documents.append(Document(page_content=doc_text, metadata={"category": category}))
            
            return FAISS.from_documents(documents, self.embeddings)
        except Exception as e:
            print(f"Error setting up knowledge base: {e}")
            # Return an empty vector store if there's an error
            return FAISS.from_documents([Document(page_content="Fallback content", metadata={"category": "general"})], self.embeddings)
    
    def generate_response(self, query, category):
        try:
            # Search for similar questions in knowledge base
            similar_docs = self.vectorstore.similarity_search(query, k=3)
            
            # Filter by category if possible
            category_docs = [doc for doc in similar_docs if doc.metadata.get("category") == category]
            if category_docs:
                similar_docs = category_docs
            
            context = "\n".join([doc.page_content for doc in similar_docs])
            
            prompt = PromptTemplate(
                input_variables=["query", "context"],
                template="Based on the following context from our knowledge base, draft a helpful response to the customer query. Be professional and helpful.\n\nContext:\n{context}\n\nQuery: {query}\n\nResponse:"
            )
            
            if self.llm:
                chain = LLMChain(llm=self.llm, prompt=prompt)
                return chain.run(query=query, context=context)
            else:
                # Fallback: return the most relevant answer from knowledge base
                if similar_docs:
                    return similar_docs[0].page_content.split("Answer: ")[-1]
                else:
                    return "I apologize, but I don't have enough information to answer your question. Please contact our support team for assistance."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again later or contact our support team directly at support@company.com."