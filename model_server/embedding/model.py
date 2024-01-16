from pydantic import BaseModel


class ExtractionResult(BaseModel):
    results: str
