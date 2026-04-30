# JobSniper AI - Backend

FastAPI backend for JobSniper AI with multi-agent architecture.

## Quick Start

1. **Install dependencies:**
```bash
pip install -e .
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. **Run the server:**
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/jobs/discover` | POST | Trigger Scout agent to find jobs |
| `/jobs/applications` | GET | List user's applications |
| `/jobs/applications/{id}/approve` | POST | Approve a job application |
| `/profile` | GET/PUT | User profile management |
| `/agents/run-pipeline` | POST | Run full agent pipeline |
| `/telegram/webhook` | POST | Telegram bot webhook |

## AI Agents

- **Scout**: Discovers jobs from Adzuna/TheirStack APIs
- **Strategist**: Scores job matches using GPT-4o
- **Ghostwriter**: Generates cover letters and tailored resumes
- **Liaison**: Drafts outreach messages to recruiters
- **Sentinel**: Monitors email for interview invites

## Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repo
3. Set build command: `pip install -e .`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`
