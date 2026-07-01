import fitz
import hashlib
from loguru import logger

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
    logger.debug("Extracted text from PDF with {} pages", len(doc))
    return text.replace('\x00', '')

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
        logger.debug("Generated SHA-256 hash for the file")
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.error("Error generating hash: {}", e)
        raise Exception(f"Error generating hash: {e}")