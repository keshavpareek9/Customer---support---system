from fastapi import FastAPI
from pydantic import BaseModel
from app import CustomerSupportSystem
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Customer Support API", description="Multi-agent customer support system")

# Add CORS middleware to allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# Initialize the support system
support_system = CustomerSupportSystem()

@app.post("/support/query")
async def process_query(request: QueryRequest):
    try:
        result = support_system.process_query(request.query)
        return result
    except Exception as e:
        return {"error": str(e), "category": "general", "response": "I apologize, but I'm experiencing technical difficulties. Please try again later."}

@app.get("/")
async def root():
    return {"message": "Customer Support API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)