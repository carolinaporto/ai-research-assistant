from loguru import logger

def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Splits the input text into chunks of specified size with optional overlap.
    Args:
        text (str): The text to be split.
        chunk_size (int): The maximum size of each chunk. Default is 1000 characters.
        overlap (int): The number of overlapping characters between consecutive chunks. Default is 200 characters.
    Returns:
        list[str]: A list of text chunks.
    """
    if chunk_size <= 0:
        logger.error("Invalid chunk_size: {}", chunk_size)
        raise ValueError("chunk_size must be a positive integer.")
    if overlap < 0:
        logger.error("Invalid overlap: {}", overlap)
        raise ValueError("overlap must be a non-negative integer.")
    if overlap >= chunk_size:
        logger.error("Invalid overlap: {}", overlap)
        raise ValueError("overlap must be less than chunk_size.")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap

    logger.debug("Text split into {} chunks", len(chunks))
    return chunks