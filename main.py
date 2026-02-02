import os
import vertexai
from flask import Flask
from vertexai.generative_models import GenerativeModel

project_id = "project-db034318-dcdd-459c-82d"
# We'll stick with us-central1 as it's the most stable for Flash
vertexai.init(project=project_id, location="us-central1")

# Change: Using the most recent "Flash" model string
model = GenerativeModel("gemini-2.0-flash-exp")

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        response = model.generate_content("Give me a one-sentence professional tip for a field service technician.")
        return f"<h1>AI Field Pilot</h1><p><b>Today's Tip:</b> {response.text}</p>"
    except Exception as e:
        # This will now give us more detail if it still fails
        return f"<h1>AI Pilot</h1><p>Status: {str(e)}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
