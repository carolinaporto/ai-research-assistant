from database import get_db
from fastapi import UploadFile, APIRouter, HTTPException, Depends
from loguru import logger
from services import ai, pdf, chunking, vector_store
from repositories import papers as papers_repo
from repositories import folders as folders_repo
from repositories import authors as authors_repo


router = APIRouter(
    prefix="/papers",
    tags=["papers"],
)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db = Depends(get_db)):
    user_id = 1  # Replace with actual user ID from authentication context
    logger.info("Upload request received: filename={}, user_id={}", file.filename, user_id)

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type. Only PDF files are allowed.")

    contents = await file.read()
    content_hash = pdf.get_paper_hash(contents)
    if papers_repo.get_paper_by_hash(db, user_id, content_hash):
        logger.warning("Duplicate upload detected: hash={}, user_id={}", content_hash, user_id)
        raise HTTPException(status_code=400, detail="This paper has already been uploaded.")

    text = pdf.extract_text(contents)
    if not text:
        logger.warning("No text extracted from PDF: filename={}", file.filename)
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")
    
    try:
        analysis = ai.summarize_text(text)

        paper_id = papers_repo.create_paper(db, user_id, file.filename, content_hash, analysis)
        papers_repo.create_paper_content(db, paper_id, text)
        logger.info("Paper saved to database: paper_id={}, user_id={}", paper_id, user_id)

        authors_repo.save_authors_for_paper(db, paper_id, analysis.authors)
        logger.info("Authors saved for paper: paper_id={}, authors={}", paper_id, analysis.authors)

        chunks = chunking.split_text(text)
        embeddings = ai.get_embeddings(chunks)
        vector_store.add_chunks(paper_id, chunks, embeddings, user_id)
        logger.info("Chunks and embeddings added to vector store: paper_id={}, num_chunks={}", paper_id, len(chunks))
        
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("Error processing upload: filename={}, user_id={}, error={}", file.filename, user_id, e)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {e}")
    
    return {"filename": file.filename, "analysis": analysis}


@router.get("/")
def get_user_papers(user_id: int, db = Depends(get_db)):
    return papers_repo.get_papers_by_user(db, user_id)


@router.get("/search")
def search_papers(user_id: int, query: str, db = Depends(get_db)):
    embeddings = ai.get_embeddings([query])[0]
    results = vector_store.search(embeddings, user_id=user_id)
    papers_ids = list({m["paper_id"] for m in results["metadatas"][0]})
    return [papers_repo.get_paper_by_id(db, user_id, paper_id) for paper_id in papers_ids]


@router.get("/{paper_id}")
def get_paper(paper_id: int, user_id: int, db = Depends(get_db)):
    paper = papers_repo.get_paper_by_id(db, user_id, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return paper


@router.delete("/{paper_id}")
def delete_paper(paper_id: int, user_id: int, db = Depends(get_db)):
    paper = papers_repo.get_paper_by_id(db, user_id, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")

    papers_repo.delete_paper(db, user_id, paper_id)
    logger.info("Paper deleted: paper_id={}, user_id={}", paper_id, user_id)
    return {"message": "Paper deleted successfully."}


@router.put("/{paper_id}/folder/{folder_id}")
def move_paper_to_folder(paper_id: int, folder_id: int, user_id: int, db = Depends(get_db)):
    paper = papers_repo.get_paper_by_id(db, user_id, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")

    folder = folders_repo.get_folder_by_id(db, user_id, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")

    papers_repo.move_paper_to_folder(db, user_id, paper_id, folder_id)
    return {"message": "Paper moved to folder successfully."}