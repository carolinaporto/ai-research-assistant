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
