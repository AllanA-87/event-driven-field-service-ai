import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def strip_code_fences(text: str) -> str:
    t = text.strip()

    # If the model wrapped JSON in ```json ... ``` or ``` ... ```
    if t.startswith("```"):
        lines = t.splitlines()

        # remove first line like ```json or ```
        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        # remove last line ```
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        t = "\n".join(lines).strip()

    return t


SYSTEM_PROMPT = """
You are an AI operations copilot for field service and manufacturing teams.
Given an enriched event payload, return practical guidance.

Return VALID JSON only with these keys:
- summary (string)
- likely_root_cause (string)
- recommended_actions (list of strings)
- next_steps (list of strings)
- questions_to_confirm (list of strings)
"""


def generate_recommendation(enriched: dict) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Return JSON only. Do not use Markdown code fences.\n\n"
                    f"Enriched event:\n{json.dumps(enriched, indent=2)}"
                ),
            },
        ],
        temperature=0.2,
    )

    raw_text = resp.choices[0].message.content
    text = strip_code_fences(raw_text)

    try:
        return json.loads(text)
    except Exception:
        return {"error": "AI did not return valid JSON", "raw": raw_text}
