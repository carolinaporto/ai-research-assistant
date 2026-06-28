from pydantic import BaseModel
from typing import List

class PaperAnalysis(BaseModel):
    authors: List[str]
    name: str
    objective: str
    summary: str
    methodology: str
    dataset: str
    main_findings: str
    limitations: str

class PaperQuestion(BaseModel):
    question_text: str
    answer_text: str

class PaperQuestions(BaseModel): 
    questions: List[PaperQuestion]
    

