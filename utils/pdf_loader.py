from PyPDF2 import PdfReader
import tempfile


def load_pdf(uploaded_file):

    text = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:

            tmp_file.write(uploaded_file.read())

            temp_path = tmp_file.name

        pdf_reader = PdfReader(temp_path)

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    except Exception as e:

        print("PDF Loading Error:", e)

    return text