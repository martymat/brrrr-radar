from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from api_errors import ApiError, error_response
from routes.properties import properties_bp
from routes.scrape import scrape_bp

app = Flask(__name__)

# Enable CORS for localhost frontend
CORS(
    app,
    origins=["http://localhost:5173"]
)

# ✅ Register blueprints BEFORE running the app
app.register_blueprint(properties_bp)
app.register_blueprint(scrape_bp)

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

@app.errorhandler(ApiError)
def handle_api_error(err: ApiError):
    payload, status = error_response(err.code, err.message, err.status, err.details)
    return jsonify(payload), status


@app.errorhandler(HTTPException)
def handle_http_exception(err: HTTPException):
    # Handles default Flask 404/405 etc in the same shape
    payload, status = error_response(
        code=err.name.upper().replace(" ", "_"),   # e.g. NOT_FOUND, METHOD_NOT_ALLOWED
        message=err.description,
        status=err.code or 500,
    )
    return jsonify(payload), status


@app.errorhandler(Exception)
def handle_unhandled_exception(err: Exception):
    # Don’t leak internals to frontend
    payload, status = error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        status=500,
    )
    # You can still log the real exception server-side:
    app.logger.exception(err)
    return jsonify(payload), status


# Optional: print routes at startup
print(app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)