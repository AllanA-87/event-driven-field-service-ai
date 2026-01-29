AI Ops Copilot - Build Notes

Goal:
Build an event-driven backend service that can receive business events (field service tickets, manufacturing quote requests), enrich them with context, and later use AI to generate recommendations.

--------------------------------------------------
FOUNDATION / BACKEND SETUP
--------------------------------------------------

- Created project structure with separate folders for:
  - backend (API + logic)
  - sample_events (demo payloads)
  - ui (future frontend)
- This mirrors real production repos and keeps concerns separated.

--------------------------------------------------
PYTHON ENVIRONMENT
--------------------------------------------------

- Created Python virtual environment using:
  python3 -m venv .venv
  source .venv/bin/activate

- Purpose:
  Isolate project dependencies so they don’t affect other projects.

--------------------------------------------------
DEPENDENCIES
--------------------------------------------------

Created requirements.txt with:

fastapi
uvicorn
pydantic
python-dotenv
requests

- FastAPI = web framework
- Uvicorn = web server
- Pydantic = data validation
- dotenv = load secrets later
- requests = make HTTP calls later

Installed dependencies with:
pip install -r requirements.txt

--------------------------------------------------
BACKEND API (FASTAPI)
--------------------------------------------------

Created app/main.py:

- Initialized FastAPI application
- Added GET /health endpoint

Purpose of /health:
Confirm backend is running and reachable.

--------------------------------------------------
EVENT CONTRACT (SCHEMA)
--------------------------------------------------

Created app/models.py with:

- EventType (allowed event names)
- Customer model
- Event model

Purpose:
Define what a valid event looks like.
FastAPI automatically validates incoming JSON.

--------------------------------------------------
EVENT RECEIVER ENDPOINT
--------------------------------------------------

Added POST /event endpoint in main.py.

What it does:
- Accepts JSON event
- Validates against Event schema
- Returns confirmation:
  received = true
  event_type
  event_id
  customer
  payload keys

Purpose:
Act as a webhook-style receiver for external systems.

--------------------------------------------------
SAMPLE EVENTS
--------------------------------------------------

Created sample JSON files:

- field_service_ticket_created.json
- manufacturing_quote_requested.json

These simulate events from:
ServiceNow / Salesforce / ERP / ticketing systems.

--------------------------------------------------
TESTING
--------------------------------------------------

Started server with:
uvicorn app.main:app --reload

Verified:
http://127.0.0.1:8000/health

Sent event using curl:
POST http://127.0.0.1:8000/event

Received successful response.

--------------------------------------------------
WHAT EXISTS NOW
--------------------------------------------------

- Running backend service
- Health check endpoint
- Event receiver endpoint
- Schema validation
- Sample events for repeatable demos

This is the backbone of an event-driven system.

--------------------------------------------------
NEXT STEP (PLANNED)
--------------------------------------------------

Add enrichment layer:
- Mock asset history
- Mock service history
- Mock parts/BOM data

Then pass enriched context to AI.
