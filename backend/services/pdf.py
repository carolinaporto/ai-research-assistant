import fitz
import hashlib

def extract_text(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file.
    Args:
        file_bytes (bytes): The bytes of the PDF file.
    Returns:
        str: The extracted text.
    """

    doc = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_paper_hash(file_bytes: bytes) -> str:
    """
    Generates a hash for the given file bytes.
    Args:
        file_bytes (bytes): The bytes of the file.
    Returns:
        str: The hash of the file.
    """
    try:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_bytes)
        return sha256_hash.hexdigest()
    except Exception as e:
        raise Exception(f"Error generating hash: {e}")