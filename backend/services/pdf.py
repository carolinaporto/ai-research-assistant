import fitz

def extract_text(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_bytes (bytes): The bytes of the PDF file.
    """

    doc = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    return text