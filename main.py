import os
import vertexai
from flask import Flask
from vertexai.generative_models import GenerativeModel

project_id = "project-db034318-dcdd-459c-82d"
# Switching to us-east1 just to bypass any local us-central1 capacity issues
vertexai.init(project=project_id, location="us-east1")

# Using the specific versioned name: gemini-1.5-flash-001
model = GenerativeModel("gemini-1.5-flash-001")

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        response = model.generate_content("Give me a one-sentence professional tip for a field service technician.")
        return f"<h1>AI Field Pilot</h1><p><b>Today's Tip:</b> {response.text}</p>"
    except Exception as e:
        return f"<h1>AI Pilot</h1><p>Error connecting to Gemini: {str(e)}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
