import os
import anthropic
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from models import ExtractRequest, InvoiceData

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

@app.post("/extract", response_model=InvoiceData)
async def extract_invoice(request: ExtractRequest):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=[tool_estrai_fattura],
        tool_choice={"type": "auto"},
        messages=[{
            "role": "user",
            "content": f"Estrai i dati da questa fattura:\n\n{request.text}"
        }]
    )

    tool_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None
    )

    if tool_block is None:
        raise HTTPException(status_code=422, detail="Claude non ha usato il tool")

    return InvoiceData(**tool_block.input)