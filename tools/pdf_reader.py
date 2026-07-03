from io import BytesIO

from PyPDF2 import PdfReader


def extract_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF.
    """

    uploaded_file.seek(0)

    reader = PdfReader(BytesIO(uploaded_file.read()))

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)
