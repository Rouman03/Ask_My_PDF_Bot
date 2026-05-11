from PyPDF2 import PdfReader


def load_pdf(uploaded_file):

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text