from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from .model import ExtractionResult
from .util import pdf_extraction_alg
import traceback
from typing import List


class Embedder:
    router: APIRouter

    def __init__(self):
        self.router = APIRouter(
            tags=["Embeddings"]
        )

        self.router.add_api_route(
            "/",
            endpoint=self.embed_file,
            methods=["POST"],
            responses={
                200: {"model": ExtractionResult},
            },
        )

    async def embed_file(
        self,
        course_code: str,
        files: List[UploadFile] = File(...)
    ):

        result_list = []
        for file in files:
            result_dict = {}
            try:
                if str(file.filename)[-4:] == ".pdf":
                    result = await pdf_extraction_alg(file)
                    result_dict = {
                        "filename": file.filename,
                        "content": result,
                    }
                result_list.append(result_dict)
            except Exception:
                print(traceback.format_exc())

        return ExtractionResult(
                results=result_list
            )


embed = Embedder()
