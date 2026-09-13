from flask import Flask, render_template, request, jsonify
from model import generate_response
import config

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    message = data.get("message")
    model_type = data.get("model")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response_data = generate_response(message, model_type)
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
