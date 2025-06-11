import os
import hashlib
import traceback

from flask import Blueprint, request, jsonify
from scripts.processor import process_pdf
from werkzeug.utils import secure_filename

pdf_routes = Blueprint("pdf_routes", __name__)


@pdf_routes.route("/test", methods=["GET"])
def test():
    return '', 200

    
@pdf_routes.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["pdf_file"]
    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Extract and validate parameters
    password = request.form.get("password", "")
    # output_name = request.form.get("output_name", "output")

    try:
        # Create the uploads directory if it doesn't exist
        upload_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Secure the filename
        pdf_path = os.path.join(upload_dir, secure_filename(pdf_file.filename))
        pdf_file.save(pdf_path)
        file_bytes = pdf_file.read()
        print("SHA256:", hashlib.sha256(file_bytes).hexdigest(), flush=True)
        pdf_file.seek(0)

        # Process the PDF
        result_json = process_pdf(pdf_path, password, "result")
        return jsonify(result_json), 200

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )