from flask import (
    Flask,
    request,
    jsonify,
    render_template
)

from werkzeug.utils import secure_filename

from services.ai_service import generate_ai_response
from services.rag_service import rag_service

from pathlib import Path
import time


app = Flask(__name__)

# Maximum uploaded file size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER = Path("data/documents")
UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Home page
# ============================================================

@app.route("/", methods=["GET"])
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# Generate AI response
# ============================================================

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json(
        silent=True
    ) or {}

    user_message = data.get("message")

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

        if not isinstance(result, dict):
            raise TypeError(
                "AI service did not return a dictionary."
            )

        result["duration"] = (
            time.time() - start_time
        )

        return jsonify(result)

    except Exception as e:

        print(
            "Error generating response:",
            repr(e)
        )

        return jsonify({
            "error": str(e)
        }), 500

# ============================================================
# Upload and index PDF
# ============================================================

@app.route("/documents/upload", methods=["POST"])
def upload_document():

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded."
        }), 400

    file = request.files["file"]

    if not file.filename:

        return jsonify({
            "error": "No file selected."
        }), 400

    # Only PDFs
    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    filename = secure_filename(
        file.filename
    )

    if not filename:

        return jsonify({
            "error": "Invalid filename."
        }), 400

    file_path = UPLOAD_FOLDER / filename

    try:

        file.save(file_path)

        # Index immediately
        chunk_count = rag_service.index_pdf(
            str(file_path)
        )

        return jsonify({
            "message": "Document uploaded and indexed successfully.",
            "document": filename,
            "chunks": chunk_count
        })

    except Exception as e:

        # Remove incomplete file if indexing fails
        if file_path.exists():
            file_path.unlink()

        print(
            "Document indexing error:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# List documents
# ============================================================

@app.route("/documents", methods=["GET"])
def list_documents():

    try:

        documents = []

        for file_path in sorted(
            UPLOAD_FOLDER.glob("*.pdf")
        ):

            documents.append({
                "name": file_path.name,
                "size": file_path.stat().st_size
            })

        return jsonify({
            "documents": documents
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# Run application
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )