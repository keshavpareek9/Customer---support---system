# Customer---support---system
A sophisticated customer support system that uses multiple specialized AI agents to classify, respond to, and review customer queries automatically.

## 🌟 Features

- **Three-Agent Architecture**: 
  - Classifier Agent: Categorizes queries into billing, technical, or general
  - Response Agent: Generates context-aware responses using knowledge base
  - Review Agent: Ensures professional tone and accuracy before sending

- **No API Dependencies**: Completely self-contained with no external API requirements
- **Streamlit Web Interface**: User-friendly chat interface
- **FastAPI Backend**: RESTful API for integration with other systems
- **Knowledge Base System**: FAQ-based response generation with similarity matching



## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI (optional)
- **AI Components**: Custom rule-based agents
- **Vector Similarity**: Keyword-based matching
- **Data Storage**: JSON-based knowledge base

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/customer-support-system.git
   cd customer-support-system
   pip install -r requirements.txt
   # Simple version (recommended)
streamlit run simple_ui.py

# Or with API backend
python api.py  # Terminal 1
streamlit run ui.py  # Terminal 2

Usage
Open the web interface (typically http://localhost:8501)

Type your customer support query in the chat input

The system will:

Classify your query (billing/technical/general)

Generate an appropriate response

Review and refine the response

Display the final answer with category information

<img width="1425" height="811" alt="Screenshot 2025-08-31 at 11 04 24 AM" src="https://github.com/user-attachments/assets/c5063e91-a567-418d-bae4-75fe631b3ab7" />

<img width="1425" height="811" alt="Screenshot 2025-08-31 at 11 04 10 AM" src="https://github.com/user-attachments/assets/93252c3b-f72e-4eed-9e71-c9f9fe874fef" />

<img width="1425" height="811" alt="Screenshot 2025-08-31 at 11 04 04 AM" src="https://github.com/user-attachments/assets/e36b2a4a-33ca-4f75-bc85-e2fa968790f3" />


