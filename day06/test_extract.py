from fastapi.testclient import TestClient
from day05.main import app

client = TestClient(app)
def test_extract_pdf_successo():
    with open("day05/fattura_test.pdf", "rb") as f:
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
def test_extract_pdf_file_mancante():
    response = client.post("/extract-pdf")
    assert response.status_code == 422
def test_extract_pdf_file_non_pdf():
    response = client.post(
        "/extract-pdf",
        files={"file": ("fake.txt", b"testo qualsiasi", "text/plain")}
    )
    
    assert response.status_code in [400, 422, 500]
