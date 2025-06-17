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

        # In-memory file stream
        file_stream = io.BytesIO(file_bytes)

        # Process the PDF
        result_json = process_pdf(file_stream)
        return jsonify(result_json), 200

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )