from flask import Blueprint, request, jsonify, send_file
from pdf_scripts.pdf_build import build_pdf
from pdf_scripts.pdf_chunk_gen import GeneratePDFChunk
from processor import process_pdf
import os
import traceback
from werkzeug.utils import secure_filename
from segregate import segregate
import json

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
        print(result_json)
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
        report = request.form.get("report", [])

    except ValueError:
        return jsonify({"error": "Threshold and lang must be valid integers"}), 400

    # ######### Proceeding to PDF Generation ######### #
    try:
        print(report)
        table_data = report.table_set1

        # result_file_path = segregate(transactions, lang)

        # ######### Proceeding to PDF Generation ######### #
        # print(result_file_path, flush=True)

        pdf_chunk = GeneratePDFChunk(
            table_set1=[
                table_data[0],
                table_data[1],
                table_data[2],
                table_data[3],
                table_data[4],
                table_data[5],
            ],
            table_set2=report.table_set2,
            pie_data=report.pie_data,
            line_data=report.line_data,
            closure=report.closure,
        )

        pdf_build_data = pdf_chunk.get_pdf_data()
        result_file_path = build_pdf(pdf_build_data)

        if result_file_path:
            # if result_file_path and os.path.exists(result_file_path):
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
