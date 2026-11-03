from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.main import app
from app.core.config import settings

import app.api.routes.document_routes as document_routes
import app.api.routes.chat_routes as chat_routes


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_documents(monkeypatch, tmp_path):

    monkeypatch.setattr(
        settings,
        "UPLOAD_DIR",
        str(tmp_path)
    )

    (tmp_path / "sample.pdf").write_bytes(b"sample")

    response = client.get("/documents/")

    assert response.status_code == 200
    assert response.json()["total_documents"] == 1


def test_invalid_upload():

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                b"Invalid file",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400


def test_successful_upload(monkeypatch, tmp_path):

    monkeypatch.setattr(
        settings,
        "UPLOAD_DIR",
        str(tmp_path)
    )

    monkeypatch.setattr(
        document_routes,
        "load_document",
        lambda path: [
            Document(page_content="Sample RAG document.")
        ]
    )

    monkeypatch.setattr(
        document_routes,
        "split_documents",
        lambda docs: docs
    )

    monkeypatch.setattr(
        document_routes,
        "add_documents",
        lambda docs: ["test-id"]
    )

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.docx",
                b"Fake DOCX content",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.docx"
    assert response.json()["chunks_created"] == 1


def test_chat(monkeypatch):

    monkeypatch.setattr(
        chat_routes,
        "answer_question",
        lambda question, k: {
            "question": question,
            "answer": "RAG combines retrieval and generation.",
            "sources": []
        }
    )

    response = client.post(
        "/chat/",
        json={
            "question": "What is RAG?",
            "k": 4
        }
    )

    assert response.status_code == 200
    assert response.json()["answer"].startswith("RAG")


def test_invalid_chat_request():

    response = client.post(
        "/chat/",
        json={
            "question": "",
            "k": 4
        }
    )

    assert response.status_code == 422


def test_delete_document(monkeypatch, tmp_path):

    monkeypatch.setattr(
        settings,
        "UPLOAD_DIR",
        str(tmp_path)
    )

    file_path = tmp_path / "sample.pdf"
    file_path.write_bytes(b"sample")

    monkeypatch.setattr(
        document_routes,
        "delete_documents_by_source",
        lambda source: 2
    )

    response = client.delete("/documents/sample.pdf")

    assert response.status_code == 200
    assert response.json()["deleted_chunks"] == 2
    assert not file_path.exists()


def test_delete_missing_document(monkeypatch, tmp_path):

    monkeypatch.setattr(
        settings,
        "UPLOAD_DIR",
        str(tmp_path)
    )

    response = client.delete("/documents/missing.pdf")

    assert response.status_code == 404