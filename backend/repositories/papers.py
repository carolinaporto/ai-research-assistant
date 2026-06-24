from datetime import datetime
from loguru import logger
from models.models import Paper, PaperContent

def get_papers_by_user(db, user_id):
    return db.query(Paper).filter(Paper.user_id == user_id).all()

def get_paper_by_id(db, user_id, paper_id):
    return db.query(Paper).filter(Paper.user_id == user_id, Paper.paper_id == paper_id).first()

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
    db.commit()
    db.refresh(paper)
    logger.info("Created paper: paper_id={}, user_id={}", paper.paper_id, user_id)
    return paper, paper.paper_id

def create_paper_content(db, paper_id: int, content: str):
    paper_content = PaperContent(paper_id=paper_id, content=content)
    db.add(paper_content)
    db.commit()
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