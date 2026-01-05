from flask import Flask, jsonify
from flask_cors import CORS
from routes.properties import properties_bp

app = Flask(__name__)

# Enable CORS for localhost frontend
CORS(
    app,
    origins=["http://localhost:5173"]
)

# ✅ Register blueprints BEFORE running the app
app.register_blueprint(properties_bp)

@app.get("/health")
def health():
    return jsonify(status="ok")

import os

@app.get("/whoami")
def whoami():
    return jsonify(
        app_file=__file__,
        pid=os.getpid(),
        routes=str(app.url_map),
    )

# Optional: print routes at startup
print(app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)