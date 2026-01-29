import json
from pathlib import Path

import requests
import streamlit as st

st.set_page_config(page_title="AI Ops Copilot", layout="wide")
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None



BACKEND_URL_DEFAULT = "http://127.0.0.1:8000"
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "sample_events"

st.title("AI Ops Copilot")
st.caption("Send an event → enrichment → AI recommendations")


# -------- Helpers --------
def load_sample(filename: str) -> dict:
    path = SAMPLES_DIR / filename
    with open(path, "r") as f:
        return json.load(f)


def post_event(backend_url: str, payload: dict) -> dict:
    url = f"{backend_url}/event"
    r = requests.post(url, json=payload, timeout=90)
    r.raise_for_status()
    return r.json()


def bullets(items):
    if not items:
        return ""
    return "\n".join([f"- {x}" for x in items])


# -------- Sidebar --------
st.sidebar.header("Settings")
backend_url = st.sidebar.text_input("Backend URL", BACKEND_URL_DEFAULT)

st.sidebar.divider()
st.sidebar.header("Event Input")

mode = st.sidebar.radio("Input mode", ["Use sample event", "Paste JSON"], index=0)

payload = None

if mode == "Use sample event":
    sample = st.sidebar.selectbox(
        "Pick a sample",
        ["field_service_ticket_created.json", "manufacturing_quote_requested.json"],
        index=0,
    )
    payload = load_sample(sample)
    st.sidebar.success(f"Loaded: {sample}")
else:
    st.sidebar.info("Paste a full JSON event payload.")
    raw = st.sidebar.text_area(
        "Event JSON",
        height=220,
        placeholder='{"event_type":"FIELD_SERVICE_TICKET_CREATED", ... }',
    )
    if raw.strip():
        try:
            payload = json.loads(raw)
            st.sidebar.success("JSON parsed successfully.")
        except Exception as e:
            st.sidebar.error(f"Invalid JSON: {e}")

st.sidebar.divider()
st.sidebar.caption("Backend should be running on :8000 and UI on :8501")


# -------- Layout --------
# -------- Layout --------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Event Payload")
    if payload:
        st.json(payload)
    else:
        st.warning("Choose a sample event or paste JSON in the sidebar.")

with col2:
    st.subheader("Result")

    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None

    send = st.button("Send Event", type="primary", disabled=(payload is None))

    # If user clicks send, call backend and store result
    if send and payload is not None:
        with st.spinner("Sending event to backend..."):
            try:
                result = post_event(backend_url, payload)
                st.session_state["last_result"] = result
                st.success("Received response from backend.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # Render tabs whenever we have a saved result
    result = st.session_state["last_result"]

    if result:
        ai = result.get("ai", {})
        enriched = result.get("enriched", {})

        tab_ai, tab_enrich, tab_raw = st.tabs(["AI Output", "Enrichment", "Raw"])

        with tab_ai:
            st.markdown("### AI Recommendations")

            if isinstance(ai, dict) and ai.get("summary"):
                st.markdown(f"**Summary**\n\n{ai.get('summary','')}")
                st.markdown(f"**Likely root cause**\n\n{ai.get('likely_root_cause','')}")

                actions = ai.get("recommended_actions", [])
                steps = ai.get("next_steps", [])
                qs = ai.get("questions_to_confirm", [])

                if actions:
                    st.markdown("**Recommended actions**")
                    st.markdown("\n".join([f"- {a}" for a in actions]))

                if steps:
                    st.markdown("**Next steps**")
                    st.markdown("\n".join([f"- {s}" for s in steps]))

                if qs:
                    st.markdown("**Questions to confirm**")
                    st.markdown("\n".join([f"- {q}" for q in qs]))

                st.divider()

                copy_text = (
                    f"Summary: {ai.get('summary','')}\n\n"
                    f"Likely root cause: {ai.get('likely_root_cause','')}\n\n"
                    "Recommended actions:\n"
                    + "\n".join([f"- {a}" for a in actions])
                    + "\n\nNext steps:\n"
                    + "\n".join([f"- {s}" for s in steps])
                    + "\n\nQuestions to confirm:\n"
                    + "\n".join([f"- {q}" for q in qs])
                )

                st.text_area("Copy-ready output", copy_text, height=220)

                st.download_button(
                    "Download AI JSON",
                    data=json.dumps(ai, indent=2),
                    file_name="ai_recommendation.json",
                    mime="application/json",
                )
            else:
                st.warning("AI output missing or malformed.")
                st.json(ai)

        with tab_enrich:
            st.markdown("### Enrichment")
            st.json(enriched)

        with tab_raw:
            st.markdown("### Full Raw Response")
            st.json(result)

