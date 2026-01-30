# AI Ops Copilot (Field Service + Manufacturing)

A demo app that receives operational events, enriches them with context (assets + service history), and uses an LLM to generate structured recommendations.

## What it does
**Event → Enrichment → AI Recommendations → UI**

- **FastAPI backend** (`/event`) validates incoming events
- **Enrichment layer** looks up related context from mock data
- **LLM layer** produces JSON recommendations (summary, root cause, actions, next steps)
- **Streamlit UI** lets you send sample events and view outputs

## 🏗️ Architecture
```mermaid
flowchart LR
    A["Event Source - Field Service and Manufacturing"] --> B["FastAPI API - POST /event"]
    B --> C["Validation and Models"]
    C --> D["Enrichment Service"]
    D --> E["Mock Asset Store"]
    D --> F["Mock Ticket History"]
    D --> G["LLM Service"]
    G --> H["OpenAI API"]
    G --> I["Structured AI Output - JSON"]
    I --> J["Streamlit UI"]


## Repo structure
- `backend/` — FastAPI + enrichment + LLM service
- `ui/` — Streamlit dashboard
- `sample_events/` — sample JSON events (field service + manufacturing)

## Prerequisites
- Python 3.12+ (you can use your installed Python)
- An OpenAI API key

## Setup (first time)
```bash
git clone <your-repo-url>
cd ai-ops-copilot

# Backend venv
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set env vars
cp .env.example .env
# edit backend/.env and add OPENAI_API_KEY=...

