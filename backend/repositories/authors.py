from loguru import logger
from models.models import Authors, PaperAuthors


def get_or_create_author(db, first_name: str, last_name: str):
    author = db.query(Authors).filter(Authors.first_name == first_name, Authors.last_name == last_name).first()
    if not author:
        author = Authors(
            first_name=first_name,
            last_name=last_name,
        )
        db.add(author)
        db.flush()
        db.refresh(author)
        logger.info("Created new author: author_id={}, first_name={}, last_name={}", author.author_id, author.first_name, author.last_name)
    else:
        logger.info("Retrieved existing author: author_id={}, first_name={}, last_name={}", author.author_id, author.first_name, author.last_name)
    return author

def associate_author_with_paper(db, author_id: int, paper_id: int):
    association = db.query(PaperAuthors).filter(PaperAuthors.author_id == author_id, PaperAuthors.paper_id == paper_id).first()
    if not association:
        association = PaperAuthors(
            author_id=author_id,
            paper_id=paper_id,
        )
        db.add(association)
        db.flush()
        logger.info("Associated author with paper: author_id={}, paper_id={}", author_id, paper_id)
    else:
        logger.info("Author already associated with paper: author_id={}, paper_id={}", author_id, paper_id)
    return association

def save_authors_for_paper(db, paper_id: int, authors_list: list):
    for author_data in authors_list:
        parts = author_data.split()
        first_name = parts[0] if parts else None
        last_name = parts[-1] if len(parts) > 1 else None
        if first_name and last_name:
            author = get_or_create_author(db, first_name, last_name)
            associate_author_with_paper(db, author.author_id, paper_id)
        else:
            logger.warning("Author data is incomplete: {}", author_data)