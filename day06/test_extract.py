from pathlib import Path
from fastapi.testclient import TestClient
from day05.main import app
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import anthropic
PDF_PATH = Path(__file__).parent.parent / "day05" / "fattura_test.pdf"

client = TestClient(app)
def test_extract_pdf_successo():
    with open(PDF_PATH, "rb") as f:
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

def test_total_amount_negativo():
   
    mock_response = MagicMock()
    mock_response.content = [MagicMock(type="tool_use", input={
        "invoice_number": "001",
        "supplier_name": "Fornitore Srl",
        "total_amount": -50.0,
        "invoice_date": "2026-01-01",
        "vat_number": "12345678901"
    })]

    with patch("day05.main.client.messages.create", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    
    assert response.status_code == 422
def test_vat_number_non_valido():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(type="tool_use", input={
        "invoice_number": "001",
        "supplier_name": "Fornitore Srl",
        "total_amount": 100.0,
        "invoice_date": "2026-01-01",
        "vat_number": "1234567890"
    })]
    with patch("day05.main.client.messages.create", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    assert response.status_code == 422

def test_invoice_date_non_valida():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(type="tool_use", input={
        "invoice_number": "001",
        "supplier_name": "Fornitore Srl",
        "total_amount": 100.0,
        "invoice_date": "01/01/2026",
        "vat_number": "12345678901"
    })]
    with patch("day05.main.client.messages.create", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    assert response.status_code == 422
def test_invoice_number_non_valido():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(type="tool_use", input={
        "invoice_number": "",
        "supplier_name": "Fornitore Srl",
        "total_amount": 100.0,
        "invoice_date": "2026-01-01",
        "vat_number": "12345678901"
    })]
    with patch("day05.main.client.messages.create", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    
    assert response.status_code == 422
def test_authentication_error():
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch("day05.main.client.messages.create",
               side_effect=anthropic.AuthenticationError(
                   message="Invalid API key",
                   response=mock_response,
                   body={"error": {"message": "Invalid API key"}}
               )):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )

    assert response.status_code == 500
    assert "autenticazione" in response.json()["detail"].lower()
def test_rate_limit_error():
    mock_response = MagicMock()
    mock_response.status_code = 429
    with patch("day05.main.client.messages.create",
               side_effect=anthropic.RateLimitError(
                   message="Rate Limit Exceeded",
                   response=mock_response,
                   body={"error": {"message": "Rate Limit Exceeded"}}
               )):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    assert response.status_code == 429
    assert "troppo" in response.json()["detail"].lower()
def test_api_error():
    mock_response = MagicMock()
    mock_response.status_code = 502
    with patch("day05.main.client.messages.create",
               side_effect=anthropic.APIError(message="Api Error" , request=MagicMock(), body=None)):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    assert response.status_code == 502
    assert "comunicazione" in response.json()["detail"].lower()
def test_validation_error_pydantic():
   
    mock_response = MagicMock()
    mock_response.content = [MagicMock(type="tool_use", input={
        "invoice_number": "001",
        "supplier_name": "Fornitore Srl",
        "total_amount": "non_numero",
        "invoice_date": "2026-01-01",
        "vat_number": "12345678901"
    })]

    with patch("day05.main.client.messages.create", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/extract-pdf",
            files={"file": ("fattura_test.pdf", open(PDF_PATH, "rb"), "application/pdf")}
        )
    
    assert response.status_code == 422
    assert "validation" in response.json()["detail"].lower()