from pydantic import BaseModel
from typing import List


class ExtractionResult(BaseModel):
    results: str


class DocumentResult(BaseModel):
    result: List


class AddSubjectParams(BaseModel):
    course_code: str
    subject_name: str


class GetCourseParams(BaseModel):
    subject_name: str


class ReturnDocumentList(BaseModel):
    documents: List
    course_code: str


class DocumentListParams(BaseModel):
    subject: str
