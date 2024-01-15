from pydantic import BaseModel
from typing import List, Dict


class ExtractionResult(BaseModel):
    results: List[Dict]
