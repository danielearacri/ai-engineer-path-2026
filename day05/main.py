import os
import anthropic
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from dotenv import load_dotenv
from day04.models import InvoiceData
from day05.pdf_extractor import extract_text_from_pdf
from datetime import date
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


load_dotenv()

app = FastAPI()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

@app.post("/extract-pdf", response_model=InvoiceData)
async def extract_invoice_from_pdf(file: UploadFile = File(...)):
    logger.info(f"File {file.filename} - {file.content_type}")
    # 1. Valida che sia un PDF
    if file.content_type != "application/pdf":
        logger.error(f"Formato non supportato: {file.content_type}. Richiesto: application/pdf")
        raise HTTPException(
            status_code=422,
            detail=f"Formato non supportato: {file.content_type}. Richiesto: application/pdf"
        )
    
    # 2. Leggi i bytes del file
    pdf_bytes = await file.read()
    

    # 3. Estrai testo con pdfplumber
    try:
        raw_text = extract_text_from_pdf(pdf_bytes)
    except ValueError as e:
        logger.error(f"Errore estrazione testo da {file.filename}: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

    # 4. Passa il testo a Claude (stessa logica di day04)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=[tool_estrai_fattura],
        tool_choice={"type": "auto"},
        messages=[{
            "role": "user",
            "content": f"Estrai i dati da questa fattura:\n\n{raw_text}"
        }]
    )

    tool_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None
    )

    if tool_block is None:
        logger.error(f"Claude non ha usato il tool {file.filename}")
        raise HTTPException(status_code=422, detail="Claude non ha usato il tool")
    logger.info(f"Claude ha usato il tool: {tool_block.input}")


    invoice = InvoiceData(**tool_block.input)
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


@app.get("/health")
async def health():
    return {"status": "ok", "model": "claude-haiku-4-5-20251001"}