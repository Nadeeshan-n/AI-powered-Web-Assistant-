from flask import Flask, request, jsonify, render_template
from services.ai_service import generate_ai_response
import time


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():

    return render_template(
        "index.html"
    )


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json(
        silent=True
    ) or {}

    user_message = data.get(
        "message"
    )

    if (
        not user_message
        or not isinstance(user_message, str)
        or not user_message.strip()
    ):

        return jsonify({
            "error": "Missing message"
        }), 400

    start_time = time.time()

    try:

        result = generate_ai_response(
            user_message.strip()
        )

        result["duration"] = (
            time.time() - start_time
        )

        return jsonify(result)

    except Exception as e:

        print(
            "Error generating response:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True
    )