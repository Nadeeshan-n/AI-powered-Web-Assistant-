from flask import Flask, render_template, request, jsonify
from model import gemini_response
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json

    user_message = data.get('message')
    model = data.get('model', 'gemini')

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    system_prompt = (
        "You are an AI assistant helping with customer inquiries. "
        "Provide a helpful and concise response."
    )

    start_time = time.time()

    try:
        if model == 'gemini':
            result = gemini_response(
                system_prompt,
                user_message
            )
        else:
            return jsonify({
                "error": "Invalid model selection"
            }), 400

        result['duration'] = time.time() - start_time

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
