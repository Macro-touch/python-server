from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
import os
import sys
import PyPDF2

def add_footer(input_pdf_path, output_pdf_path, footer_text, page_text, optional_text):
    # Create a new PDF for the footer
    footer_pdf_path = input_pdf_path.replace(".pdf", "_footer.pdf")
    footer_canvas = canvas.Canvas(footer_pdf_path, pagesize=letter)

    # Get the number of pages
    pdf_reader = PyPDF2.PdfReader(input_pdf_path)
    num_pages = len(pdf_reader.pages)

    # Add footer on each page
    for page_num in range(num_pages):
        footer_canvas.setFont("Helvetica", 9)
        # Bottom left: "Macrotouch"
        footer_canvas.drawString(30, 15, footer_text)

        # Bottom center: Page number
        footer_canvas.drawString(275, 15, f"Page {page_num + 1} of {num_pages}")

        # Bottom right: Optional text
        if optional_text:
            footer_canvas.drawString(500, 15, optional_text)

        footer_canvas.showPage()

    footer_canvas.save()

    # Merge the footer with the original PDF
    pdf_writer = PyPDF2.PdfWriter()
    footer_reader = PyPDF2.PdfReader(footer_pdf_path)

    for page_num, page in enumerate(pdf_reader.pages):
        page.merge_page(footer_reader.pages[page_num])
        pdf_writer.add_page(page)

    # Write the merged PDF to the output
    with open(output_pdf_path, "wb") as output_file:
        pdf_writer.write(output_file)

    os.remove(footer_pdf_path)


def build_pdf(data, file_id, company_name):
    # Creating a table PDF
    pdf_path = sys.path[0] + "/table.pdf"
    document = SimpleDocTemplate(pdf_path, pagesize=letter)
    document.build(data)

    # Making Reports Directory
    pdf_files = [pdf_path]
    report_dir = "Reports " + file_id
    os.makedirs(report_dir, exist_ok=True)

    # Creating and merging the report file with table PDF
    report_path = "report.pdf"
    output_pdf = os.path.join(report_dir + "/" + report_path)

    pdf_merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)

    with open(output_pdf, "wb") as output_file:
        pdf_merger.write(output_file)

    pdf_merger.close()
    os.remove(pdf_path)

    # Add footer to the final report
    add_footer(
        input_pdf_path=output_pdf,
        output_pdf_path=output_pdf,
        footer_text="Macrotouch",
        page_text="Page",
        optional_text=company_name
    )

    return output_pdf
