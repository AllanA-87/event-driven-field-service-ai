## 🚀 The Architecture
* **Frontend:** Python Flask (Serverless)
* **AI Brain:** Vertex AI (Gemini API)
* **Deployment:** Google Cloud Build (CI/CD)
* **Hosting:** Google Cloud Run (Auto-scaling)

## ⚠️ The "Locked Down" Reality (Read This First!)
Google Cloud Services are **locked down by default**. If you see 403 (Forbidden) or 404 (Not Found) errors, **do not be alarmed.** You are on the right track! 

### How to Navigate Permission Hurdles:
1. **Enable the APIs:** You must explicitly turn on the `aiplatform.googleapis.com` and `run.googleapis.com` services.
2. **Assign Specific Roles:** Your Cloud Run service account needs the `Vertex AI User` role.
3. **The "ActAs" Permission:** You must give your own user account the `Service Account User` role to "pass" that identity to the cloud service.
4. **Leverage Gemini:** If a log message looks like Greek, copy-paste it into the Google Cloud AI Chat. It will guide you to the specific IAM toggle you missed.



## 🛠️ Setup & Deployment
1. **Clone the Repo**
2. **Set your Project ID** in `main.py`.
3. **Deploy via Cloud Shell:**
   ```bash
   gcloud run deploy copilot-service --source . --region us-central1








# AI Ops Copilot (Field Service + Manufacturing) 

A demo app that receives operational events, enriches them with context (assets + service history), and uses an LLM to generate structured recommendations.

## What it does
**Event → Enrichment → AI Recommendations → UI**

- **FastAPI backend** (`/event`) validates incoming events
- **Enrichment layer** looks up related context from mock data
- **LLM layer** produces JSON recommendations (summary, root cause, actions, next steps)
- **Streamlit UI** lets you send sample events and view outputs

## 🏗️ Architecture
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

