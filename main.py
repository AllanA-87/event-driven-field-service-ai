import os
import vertexai
from flask import Flask
from vertexai.generative_models import GenerativeModel

project_id = "project-db034318-dcdd-459c-82d"
vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-2.0-flash-exp")

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Field Pilot</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a2e; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: #16213e; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; max-width: 500px; border: 1px solid #0f3460; }
        h1 { color: #4ecca3; margin-bottom: 0.5rem; }
        p { font-size: 1.2rem; line-height: 1.6; color: #e94560; font-weight: bold; }
        .footer { margin-top: 2rem; font-size: 0.8rem; color: #95a5a6; }
        button { background-color: #4ecca3; border: none; padding: 10px 20px; border-radius: 5px; color: #1a1a2e; font-weight: bold; cursor: pointer; margin-top: 1rem; }
        button:hover { background-color: #45b791; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🛠️ AI Field Pilot</h1>
        <hr style="border: 0.5px solid #0f3460;">
        <h3>Today's Safety & Tech Tip:</h3>
        <p>{tip}</p>
        <button onclick="window.location.reload();">Get New Tip</button>
        <div class="footer">Powered by Google Vertex AI & Cloud Run</div>
    </div>
</body>
</html>
"""

@app.route("/")
def hello():
    try:
        response = model.generate_content("Give me a one-sentence professional tip for a field service technician.")
        return HTML_TEMPLATE.format(tip=response.text)
    except Exception as e:
        return f"<h1>AI Pilot</h1><p>Error: {str(e)}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
