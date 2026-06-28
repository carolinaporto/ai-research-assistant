from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from repositories import questions as questions_repo, papers as papers_repo
from services.ai import generate_questions

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)

@router.post("/")
async def create_question(paper_id: int, db = Depends(get_db)):
    logger.info("Create question request received: paper_id={}", paper_id)
    # Here you would typically call a service to generate the question and answer
    # For demonstration, let's assume we have a function `generate_question_and_answer`
    text = papers_repo.get_paper_content_by_id(db, paper_id)
    if not text:
        logger.error("Paper not found for paper_id={}", paper_id)
        raise HTTPException(status_code=404, detail="Paper not found.")
    
    existing = questions_repo.get_questions_by_paper_id(db, paper_id)
    if existing:
        logger.info("Questions already exist for paper_id={}", paper_id)
        return existing 

    result = generate_questions(text)
    for q in result.questions:
        question = questions_repo.create_question(db, paper_id, q.question_text, q.answer_text)
        if not question:
            logger.error("Failed to create question for paper_id={}", paper_id)
            raise HTTPException(status_code=500, detail="Failed to create question.")

    logger.info("Questions created successfully for paper_id={}", paper_id)
    return questions_repo.get_questions_by_paper_id(db, paper_id)

@router.get("/{paper_id}")
async def get_questions(paper_id: int, db = Depends(get_db)):
    logger.info("Get questions request received: paper_id={}", paper_id)
    questions = questions_repo.get_questions_by_paper_id(db, paper_id)
    return questions

@router.delete("/{question_id}")
async def delete_question(question_id: int, db = Depends(get_db)):
    logger.info("Delete question request received: question_id={}", question_id)
    deleted_question = questions_repo.delete_question(db, question_id)
    if deleted_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}


@router.delete("/paper/{paper_id}/all")
async def delete_all_paper_questions(paper_id: int, db = Depends(get_db)):
    logger.info("Delete all questions request received: paper_id={}", paper_id)
    deleted_count = questions_repo.delete_all_paper_questions(db, paper_id)
    return {"message": f"Deleted {deleted_count} questions for paper_id={paper_id}"}