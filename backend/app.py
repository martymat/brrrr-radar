from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for localhost frontend
CORS(
    app,
    origins=["http://localhost:5173"]
)

@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)