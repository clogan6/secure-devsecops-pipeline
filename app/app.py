from flask import Flask, jsonify, request
import os
import re

# Create the Flask application
app = Flask(__name__)

# Read debug config from environment
debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# Security Checks
def security_checks(user):
    if not len(user) <= 50 and len(user) >=1:
        raise ValueError("Username must be between 1 and 50 characters")
    if not re.fullmatch(r"[A-Za-z0-9 _-]+", user):
        raise ValueError("Invalid characters")
    return user

@app.errorhandler(ValueError)
def input_failure(e):
    return jsonify({
        "error": "Bad Request",
        "message": str(e)
    }), 400

# Apply security headers to outgoing responses
@app.after_request
def apply_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response

# Define a health-check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "application": "Secure DevSecOps Pipeline"
    }), 200

# Creating an endpoint to receive user data
@app.route("/greet", methods=["GET"])
def greet_user():
    user = request.args.get('user')
    if user is None:
        raise ValueError("Must include user parameter")
    user = user.strip()
    user = security_checks(user)
    return jsonify({
        "message": f"Hello, {user}!"
    }), 200

# Start the development server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
