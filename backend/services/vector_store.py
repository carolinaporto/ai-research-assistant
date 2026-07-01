import chromadb
from loguru import logger

client = chromadb.PersistentClient(path="chroma_db")

def get_collection():
    """ 
    Returns the "papers" collection from ChromaDB. If it doesn't exist, it creates a new collection named "papers".
    This collection is used to store and manage chunks of text related to academic papers, along with their embeddings and metadata.
    Returns:
        chromadb.api.models.Collection.Collection: The "papers" collection from ChromaDB.
    """ 
    logger.debug("Accessing the 'papers' collection in ChromaDB")
    return client.get_or_create_collection("papers")

def add_chunks(paper_id: int, chunks: list[str], embeddings: list[list[float]], user_id: int):
    """ 
    Adds chunks of text and their corresponding embeddings to the "papers" collection in ChromaDB.
    Each chunk is associated with a unique ID and metadata that includes the paper ID.
    Args:
        paper_id (int): The ID of the paper to which the chunks belong.
        chunks (list[str]): A list of text chunks to be added to the collection.
        embeddings (list[list[float]]): A list of embeddings corresponding to each chunk.
        user_id (int): The ID of the user who owns the paper.
    """
    collection = get_collection()
    ids = [f"paper_{paper_id}_chunk_{i}" for i, _ in enumerate(chunks)]
    metadatas = [{"paper_id": paper_id, "user_id": user_id} for _ in chunks]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    logger.debug("Added {} chunks for paper_id={}", len(chunks), paper_id)

def search(query_embedding: list[float], n_results: int = 5, user_id: int = None):
    """ 
    Searches for the most similar chunks to the given query embedding in the "papers" collection.
    Args:
        query_embedding (list[float]): The embedding of the query.
        n_results (int): The number of results to return.
        user_id (int): The ID of the user who owns the paper.   
    Returns:
        chromadb.api.models.Results.Results: The search results from ChromaDB.
    """
    collection = get_collection()
    logger.debug("Searching for the top {} results in the 'papers' collection", n_results)
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"user_id": user_id}  # Filter by user_id to ensure user-specific search
    )
