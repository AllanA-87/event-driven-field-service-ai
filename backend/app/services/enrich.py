import json
from pathlib import Path
from app.models import Event

# Path to app/data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_json(filename: str):
    path = DATA_DIR / filename
    with open(path, "r") as f:
        return json.load(f)

def enrich_event(event: Event) -> dict:
    assets_db = load_json("mock_assets.json")
    ticket_history_db = load_json("mock_ticket_history.json")

    account_id = event.customer.account_id

    enriched = {
        "event": event.model_dump(),
        "customer_assets": assets_db.get(account_id, {}).get("assets", []),
        "asset_history": []
    }

    # If field service ticket, attach asset history
    if event.event_type == "FIELD_SERVICE_TICKET_CREATED":
        asset_id = event.payload.get("asset", {}).get("asset_id")
        if asset_id:
            enriched["asset_history"] = ticket_history_db.get(asset_id, [])

    return enriched
