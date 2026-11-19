from flask import Flask, jsonify

# Create the Flask application
app = Flask(__name__)

# Define a health-check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "application": "Secure DevSecOps Pipeline"
    }), 200


# Start the development server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
