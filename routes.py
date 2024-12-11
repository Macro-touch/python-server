from flask import Blueprint, request, jsonify, send_file
from processor import process_pdf
import os
import traceback
from werkzeug.utils import secure_filename
from segregate import segregate

pdf_routes = Blueprint("pdf_routes", __name__)


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

        # Process the PDF
        result_json = process_pdf(pdf_path, password, "result")
        return jsonify(result_json), 200

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


@pdf_routes.route("/create-pdf", methods=["POST"])
def create_pdf():

    # ######### Extract and validate parameters ######### #
    try:
        data = request.form.get("transactions", [])
        threshold = int(request.form.get("threshold", 0))
        lang = int(request.form.get("language", 0))

    except ValueError:
        return jsonify({"error": "Threshold and lang must be valid integers"}), 400

    # ######### Proceeding to PDF Generation ######### #
    try:
        print(data)
        result_file_path = segregate(data, threshold, lang)

        # ######### Proceeding to PDF Generation ######### #
        if result_file_path and os.path.exists(result_file_path):
            return send_file(
                result_file_path,
                as_attachment=True,
                mimetype="application/pdf",
                download_name="report.pdf",
            )
        else:
            return jsonify({"error": "File generation failed"}), 500

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"error": "Error processing PDF", "details": str(e)}),
            500,
        )
