from pydantic import BaseModel, Field
from typing import Optional

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Testo della fattura da analizzare")

class InvoiceData(BaseModel):
    invoice_number: str = Field(..., description="Numero fattura")
    supplier_name: str = Field(..., description="Nome fornitore o emittente")
    total_amount: float = Field(..., description="Importo totale in euro")
    invoice_date: Optional[str] = Field(None, description="Data fattura in formato ISO 8601")
    vat_number: Optional[str] = Field(None, description="Partita IVA del fornitore")