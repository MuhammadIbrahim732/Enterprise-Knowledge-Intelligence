from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# Test root endpoint
response = client.get("/")

print("\nROOT ENDPOINT:")
print(response.status_code)
print(response.json())

assert response.status_code == 200


# Test health endpoint
response = client.get("/health")

print("\nHEALTH ENDPOINT:")
print(response.status_code)
print(response.json())

assert response.status_code == 200


# Test document listing
response = client.get("/documents/")

print("\nDOCUMENT LIST ENDPOINT:")
print(response.status_code)
print(response.json())

assert response.status_code == 200


# Test invalid file upload
response = client.post(
    "/documents/upload",
    files={
        "file": (
            "invalid.txt",
            b"Sample text",
            "text/plain"
        )
    }
)

print("\nINVALID UPLOAD TEST:")
print(response.status_code)
print(response.json())

assert response.status_code == 400


print("\nAll API integration tests passed!")