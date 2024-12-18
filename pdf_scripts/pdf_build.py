import sys, os, PyPDF2
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
import time

def current_milli_time():
    return round(time.time() * 1000)


def build_pdf(data):

    # creating a table pdf alone first
    pdf_path = sys.path[0] + '/table.pdf'
    document = SimpleDocTemplate(pdf_path, pagesize=letter)
    document.build(data)

    # making Reports Directory
    pdf_files = [sys.path[0] + '/cover.pdf', pdf_path]
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)

    # creating a merging the report file with table pdf
    report_path = 'report.pdf'
    output_pdf = os.path.join(report_dir + '/' + report_path)

    pdf_merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)

    with open(output_pdf, "wb") as output_file:
        pdf_merger.write(output_file)

    pdf_merger.close()
    os.remove(pdf_path)
