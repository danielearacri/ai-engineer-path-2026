from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Fattura(BaseModel):
    fornitore: str
    importo: float
    data: str
    note: Optional[str] = None
    numero_fattura: str
    iva: Optional[float] = 0.22
@app.post("/estrai-fattura")
async def crea_fattura(fattura: Fattura):
    return fattura.model_dump()
   