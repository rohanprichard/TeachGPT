from pydantic import BaseModel
from typing import List, Dict


class ExtractionResult(BaseModel):
    results: str


class DocumentResult(BaseModel):
    result: List[Dict]
