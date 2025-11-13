# Dumroo Admin Panel - AI Query System

AI-powered natural language query system for educational admin panels with role-based access control.

## Features

-  Natural language queries using LangChain + OpenAI GPT-3.5
-  Role-based access control (admins see only their grade/region data)
-  Conversational AI with memory for follow-up questions
-  Modular design - easy to connect to real databases
-  Streamlit interface

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key

**Important:** The current API key has exceeded its quota.

Update `.env` file with a valid OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

Get credits at: https://platform.openai.com/account/billing

### 3. Run
```bash
streamlit run app.py
```

Open: http://localhost:8501

## Usage

### Demo Admins

| Admin | Grade | Region | Access |
|-------|-------|--------|--------|
| admin1 (John Doe) | 8 | North | 4 students, 2 quizzes |
| admin2 (Jane Smith) | 9 | South | 2 students, 1 quiz |
| admin3 (Mike Johnson) | 7 | East | 2 students, 1 quiz |

### Example Queries

- "Which students haven't submitted their homework yet?"
- "Show me performance data for Grade 8"
- "List all upcoming quizzes"
- "Who are my students?"

## Architecture

```
├── app.py                  # Streamlit UI
├── query_agent.py          # LangChain AI agent
├── data_manager.py         # Data access with RBAC
├── access_control.py       # Role management
├── config.py               # Configuration
├── data.json               # Sample dataset
└── test_system.py          # Tests
```

## Testing

```bash
python test_system.py
```

## Docker

```bash
docker-compose up -d
```

## Tech Stack

- Python 3.11+
- LangChain 0.1.13
- OpenAI GPT-3.5-turbo
- Streamlit 1.32.0
- Pandas 2.2.1

## Database Integration

Currently uses JSON. To connect to PostgreSQL:

```python
# In data_manager.py
from sqlalchemy import create_engine

class DataManager:
    def __init__(self, db_url=None):
        if db_url:
            self.engine = create_engine(db_url)
            # Load from database
```

Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dumroo
```

## Troubleshooting

**API key quota exceeded:** Add credits at https://platform.openai.com/account/billing

**Module not found:** Run `pip install -r requirements.txt`

**Port in use:** Run `streamlit run app.py --server.port=8502`

---

**Status:** Production Ready  
**Version:** 1.0.0
