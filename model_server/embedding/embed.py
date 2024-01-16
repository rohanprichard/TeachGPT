from fastapi.routing import APIRouter
from .model import ExtractionResult
from fastapi import UploadFile, File
from .util import pdf_extraction_alg
from typing import List
import traceback
import logging
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Embedder:
    router: APIRouter

    def __init__(self):

        self.logger = logging.getLogger(f"{__name__}")
        logging.basicConfig()
        self.logger.setLevel(logging.DEBUG)

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
        self.router.add_api_route(
            "/test",
            endpoint=self.query,
            methods=["POST"],
        )

        self.logger.info("initialized embeddings route")

        self._client = chromadb.PersistentClient(path="./chroma-vectorstore")
        self._collection = self._client.get_or_create_collection(
            "vectorstore-15-1-24"
            )

    async def embed_file(
        self,
        files: List[UploadFile] = File(...)
    ):

        result_list = []
        self.logger.info(f"recieved {len(files)} files")
        for file in files:
            result_dict = {}
            try:
                if str(file.filename)[-4:] == ".pdf":
                    result = await pdf_extraction_alg(file)
                    result_dict = {
                        "filename": file.filename[8:],  # type: ignore
                        "content": result,  # f"{len(result)} characters",
                        "course_code": file.filename[:8]  # type: ignore
                    }
                    self.logger.debug(
                        f"{len(result)} characters from {file.filename}"
                        )

                self.add_document(result_dict)

                result_list.append(result_dict)

            except Exception:
                print(traceback.format_exc())

        return ExtractionResult(
                results=f"{len(result_list)} files added."
            )

    def add_document(self, extracted):
        self.logger.debug("Initializing Text splitter")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        self.logger.debug("Creating documents of 1500 chars")
        docs = text_splitter.create_documents([extracted['content']])

        self.logger.debug(
            f"Adding {len(docs)} documents of 1500 chars to vectorstore"
            )
        self._collection.add(
            documents=[d.page_content for d in docs],
            metadatas=[{
                "source": extracted['filename'],
                "course_code": extracted['course_code']
                } for d in docs],
            ids=[
                (f"{extracted['course_code']}-{extracted['filename']}-"
                 + str(i)) for i in range(len(docs))],
        )

    def query(self, message, course_id):
        results = self._collection.query(
            query_texts=[message],
            n_results=1,
            where={"course_code": course_id},
        )

        self.logger.debug(f"Search results: {results}")

        if len(results['distances'][0]) != 0:  # type: ignore
            self.logger.debug(f"Confidence: {results}")
            if results['distances'][0][0] > 0.3:  # type: ignore
                return (
                    str(results['documents'][0][0]),  # type: ignore
                    str(results['metadatas'][0][0]['source'])  # type: ignore
                )

        return ("", "")


embedder = Embedder()
