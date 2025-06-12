import hashlib
import traceback
import requests
import io

from flask import Blueprint, request, jsonify
from scripts.processor import process_pdf

pdf_routes = Blueprint("pdf_routes", __name__)


@pdf_routes.route("/test", methods=["GET"])
def test():
    return '', 200

    
@pdf_routes.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    # if "pdf_file" not in request.files:
    #     return jsonify({"error": "No file part"}), 400

    # pdf_file = request.files["pdf_file"]
    # if pdf_file.filename == "":
    #     return jsonify({"error": "No selected file"}), 400

    # # Extract and validate parameters
    # password = request.form.get("password", "")
    # # output_name = request.form.get("output_name", "output")

    # try:
    #     # Create the uploads directory if it doesn't exist
    #     upload_dir = os.path.join(os.getcwd(), "uploads")
    #     os.makedirs(upload_dir, exist_ok=True)

    #     # Secure the filename
    #     pdf_path = os.path.join(upload_dir, secure_filename(pdf_file.filename))
    #     pdf_file.save(pdf_path)
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        pdf_url = data.get("pdf_file")
        password = data.get("password", "")

        if not pdf_url:
            return jsonify({"error": "No PDF URL provided"}), 400

        # Download the file from the URL
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF file"}), 400

        file_bytes = response.content

        # SHA256 checksum (optional)
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        print("SHA256:", sha256, flush=True)

        # In-memory file stream
        file_stream = io.BytesIO(file_bytes)

        # Process the PDF
        result_json = process_pdf(file_stream, password, "result")
        return jsonify(result_json), 200

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )