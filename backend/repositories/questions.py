from models.models import Question
from datetime import datetime
from loguru import logger

def get_questions_by_paper_id(db, paper_id):
    return db.query(Question).filter(Question.paper_id == paper_id).all()

def create_question(db, paper_id, question_text, answer_text):
    question = Question(
        paper_id=paper_id,
        question_text=question_text,
        answer_text=answer_text,
        created_at=datetime.utcnow()
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    logger.info("Created question: question_id={}, paper_id={}", question.question_id, paper_id)
    return question

def delete_question(db, question_id):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        logger.warning("Question not found for deletion: question_id={}", question_id)
        return None
    db.delete(question)
    db.commit()
    logger.info("Deleted question: question_id={}", question_id)
    return question

def delete_all_paper_questions(db, paper_id):
    questions = db.query(Question).filter(Question.paper_id == paper_id).all()
    deleted_count = len(questions)
    for question in questions:
        db.delete(question)
    db.commit()
    logger.info("Deleted all questions for paper_id={}: count={}", paper_id, deleted_count)
    return deleted_count