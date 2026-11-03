from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.services.document_loader import load_document
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents
from app.schemas.api_schemas import UploadResponse
from app.services.vector_store import delete_documents_by_source


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):

    allowed_extensions = {".pdf", ".docx"}

    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if not filename or extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load document
        documents = load_document(str(file_path))

        # Validate extracted content
        if not any(document.page_content.strip() for document in documents):
            raise HTTPException(
                status_code=400,
                detail="The uploaded document contains no readable text."
            )

        # Split into chunks
        chunks = split_documents(documents)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be generated."
            )

        # Store in ChromaDB
        add_documents(chunks)

        return UploadResponse(
            filename=filename,
            message="Document uploaded and indexed successfully.",
            chunks_created=len(chunks)
        )

    except HTTPException:
        raise

    except Exception as error:
        # Remove incomplete upload if processing fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        )

    finally:
        file.file.close()


@router.get("/")
def list_documents():

    upload_dir = Path(settings.UPLOAD_DIR)

    upload_dir.mkdir(parents=True, exist_ok=True)

    documents = []

    for file_path in upload_dir.iterdir():

        if file_path.is_file() and file_path.suffix.lower() in {".pdf", ".docx"}:

            documents.append({
                "filename": file_path.name,
                "file_type": file_path.suffix.lower().replace(".", ""),
                "size_bytes": file_path.stat().st_size
            })

    return {
        "total_documents": len(documents),
        "documents": documents
    }

@router.delete("/{filename}")
def delete_document(filename: str):

    upload_dir = Path(settings.UPLOAD_DIR)

    # Prevent directory traversal
    if Path(filename).name != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    file_path = upload_dir / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:
        # Delete document chunks from ChromaDB
        deleted_chunks = delete_documents_by_source(filename)

        # Delete physical file
        file_path.unlink()

        return {
            "message": "Document deleted successfully.",
            "filename": filename,
            "deleted_chunks": deleted_chunks
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document deletion failed: {str(error)}"
        )