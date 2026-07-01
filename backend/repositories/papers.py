from datetime import datetime
from loguru import logger
from services import vector_store
from models.models import Paper, PaperContent, PaperAuthors, Question

def get_papers_by_user(db, user_id):
    return db.query(Paper).filter(Paper.user_id == user_id).all()

def get_paper_by_id(db, user_id, paper_id):
    return db.query(Paper).filter(Paper.user_id == user_id, Paper.paper_id == paper_id).first()

def get_paper_content_by_id(db, paper_id):
    paper_content = db.query(PaperContent).filter(PaperContent.paper_id == paper_id).first()
    if paper_content:
        return paper_content.content
    else:
        logger.warning("Paper content not found for paper_id={}", paper_id)
        return None

def get_paper_by_hash(db, user_id, content_hash):
    return db.query(Paper).filter(Paper.user_id == user_id, Paper.content_hash == content_hash).first()

def create_paper(db, user_id, filename, content_hash, analysis):
    paper = Paper(
        user_id=user_id,
        filename=filename,
        content_hash=content_hash,
        uploaded_at=datetime.utcnow(),
        name=analysis.name,
        objective=analysis.objective,
        summary=analysis.summary,
        methodology=analysis.methodology,
        dataset=analysis.dataset,
        main_findings=analysis.main_findings,
        limitations=analysis.limitations,
    )
    db.add(paper)
    db.flush()
    db.refresh(paper)
    logger.info("Created paper: paper_id={}, user_id={}", paper.paper_id, user_id)
    return paper.paper_id

def delete_paper(db, user_id, paper_id):
    paper = get_paper_by_id(db, user_id, paper_id)
    if paper:
        for q in db.query(Question).filter(Question.paper_id == paper_id).all():
            db.delete(q)
        db.flush()

        for pa in db.query(PaperAuthors).filter(PaperAuthors.paper_id == paper_id).all():
            db.delete(pa)
        db.flush()

        content = db.query(PaperContent).filter(PaperContent.paper_id == paper_id).first()
        if content:
            db.delete(content)
        db.flush()

        chroma_collection = vector_store.get_collection()
        chroma_collection.delete(where={"paper_id": paper_id})
        logger.debug("Deleted chunks from vector store for paper_id={}", paper_id)

        db.delete(paper)
        db.commit()
        logger.info("Deleted paper: paper_id={}, user_id={}", paper_id, user_id)
    else:
        logger.warning("Attempted to delete non-existent paper: paper_id={}, user_id={}", paper_id, user_id)


def create_paper_content(db, paper_id: int, content: str):
    paper_content = PaperContent(paper_id=paper_id, content=content)
    db.add(paper_content)
    db.flush()
    logger.debug("Saved raw text for paper_id={}", paper_id)

def move_paper_to_folder(db, user_id, paper_id, folder_id):
    paper = get_paper_by_id(db, user_id, paper_id)
    if not paper:
        logger.warning("Paper not found for move operation: paper_id={}, user_id={}", paper_id, user_id)
        return None
    paper.folder_id = folder_id
    db.commit()
    logger.info("Moved paper to folder: paper_id={}, folder_id={}, user_id={}", paper_id, folder_id, user_id)
    return paper