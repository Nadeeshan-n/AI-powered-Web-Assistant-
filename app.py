from flask import Flask, request, jsonify, render_template
from services.ai_service import generate_ai_response

import time

app = Flask(__name__)


# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Generate AI response
@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    user_message = data.get("message")
    model = data.get("model", "gemini")

    # Validate message
    if not user_message:
        return jsonify({
            "error": "Missing message"
        }), 400

    # System prompt
    system_prompt = (
        "You are an AI assistant helping with customer inquiries. "
        "Provide a helpful and concise response."
    )

    start_time = time.time()

    try:

        # Select model
        if model == "gemini":

           result = generate_ai_response(user_message)

        else:

            return jsonify({
                "error": "Invalid model selection"
            }), 400

        # Calculate response duration
        result["duration"] = time.time() - start_time

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)