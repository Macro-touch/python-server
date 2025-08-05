from pypdf import PdfReader, PdfWriter
import io

from scripts.processor import process_pdf

def unlock_pdf(file_stream, password=None):
    file_stream.seek(0)
    reader = PdfReader(file_stream)

    if reader.is_encrypted:
        if password:
            reader.decrypt(password)
        else:
            raise Exception("Error unlocking pdf.")

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return process_pdf(output_stream)
