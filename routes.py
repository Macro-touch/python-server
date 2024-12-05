from flask import Blueprint, request, jsonify
from processor import process_pdf
import os

pdf_routes = Blueprint("pdf_routes", __name__)


@pdf_routes.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    # Ensure that a file is provided
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["pdf_file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Extract parameters from the request
    password = request.form.get("password", "")
    output_name = request.form.get("output_name", "output")
    threshold = int(request.form.get("threshold", 0))
    lang = int(request.form.get("lang", 0))

    try:
        # Save the uploaded PDF to the server
        pdf_path = os.path.join("uploads", pdf_file.filename)
        pdf_file.save(pdf_path)

        # Process the PDF
        result_json = process_pdf(pdf_path, password, output_name, threshold, lang)

        return jsonify(result_json), 200

    except Exception as e:

        print(type(e).with_traceback())

        return jsonify({"error": str(e)}), 500
