import os
import anthropic
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from dotenv import load_dotenv
from day04.models import InvoiceData
from day05.pdf_extractor import extract_text_from_pdf
from datetime import date
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tool_estrai_fattura = {
    "name": "estrai_dati_fattura",
    "description": "Estrai i dati strutturati da una fattura italiana.",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string", "description": "Numero fattura"},
            "supplier_name": {"type": "string", "description": "Nome fornitore"},
            "total_amount": {"type": "number", "description": "Importo totale in euro"},
            "invoice_date": {"type": "string", "description": "Data fattura ISO 8601"},
            "vat_number": {"type": "string", "description": "Partita IVA fornitore"}
        },
        "required": ["invoice_number", "supplier_name", "total_amount"]
    }
}


async def extract_invoice_from_bytes(pdf_bytes: bytes) -> InvoiceData:
    try:
        raw_text = extract_text_from_pdf(pdf_bytes)
    except ValueError as e:
        logger.error(f"Errore estrazione testo: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=[tool_estrai_fattura],
            tool_choice={"type": "auto"},
            messages=[{
                "role": "user",
                "content": f"Estrai i dati da questa fattura:\n\n{raw_text}"
            }]
        )
    except anthropic.AuthenticationError as e:
        logger.error(f"Errore autenticazione API: {str(e)}")
        raise HTTPException(status_code=500, detail="Errore di autenticazione API")
    except anthropic.RateLimitError as e:
        logger.error(f"Rate limit superato: {str(e)}")
        raise HTTPException(status_code=429, detail="Troppo richieste, riprovare")
    except anthropic.APIError as e:
        logger.error(f"Errore comunicazione Claude: {str(e)}")
        raise HTTPException(status_code=502, detail="Errore comunicazione con Claude")

    tool_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None
    )

    if tool_block is None:
        logger.error("Claude non ha usato il tool")
        raise HTTPException(status_code=422, detail="Claude non ha usato il tool")
    logger.info(f"Claude ha usato il tool: {tool_block.input}")

    try:
        invoice = InvoiceData(**tool_block.input)
    except ValidationError as e:
        logger.error(f"Formato dati non valido: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    if invoice.total_amount <= 0:
        logger.error(f"Importo totale non valido: {invoice.total_amount}")
        raise HTTPException(status_code=422, detail="Importo totale non valido")
    if invoice.vat_number:
        if len(invoice.vat_number) != 11 or not invoice.vat_number.isdigit():
            logger.error(f"Partita IVA non valida: {invoice.vat_number}")
            raise HTTPException(status_code=422, detail="Partita IVA non valida: deve essere 11 cifre numeriche")
    if invoice.invoice_date:
        try:
            date.fromisoformat(invoice.invoice_date)
        except ValueError:
            logger.error(f"Data fattura non valida: {invoice.invoice_date}")
            raise HTTPException(status_code=422, detail="Data fattura non valida: deve essere in formato ISO 8601")
    if not invoice.invoice_number.strip():
        logger.error(f"Numero fattura non valido: {invoice.invoice_number}")
        raise HTTPException(status_code=422, detail="Numero fattura non valido")

    return invoice


@app.post("/extract-pdf", response_model=InvoiceData)
async def extract_invoice_from_pdf(file: UploadFile = File(...)):
    logger.info(f"File {file.filename} - {file.content_type}")
    if file.content_type != "application/pdf":
        logger.error(f"Formato non supportato: {file.content_type}")
        raise HTTPException(status_code=422, detail="Formato non supportato")
    pdf_bytes = await file.read()
    return await extract_invoice_from_bytes(pdf_bytes)


@app.get("/health")
async def health():
    return {"status": "ok", "model": "claude-haiku-4-5-20251001"}