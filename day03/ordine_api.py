from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Ordine(BaseModel):
    cliente: str
    prodotto: str
    quantita: int
    sconto: Optional[float] = 0.0
@app.post("/ordine")
async def crea_ordine(ordine: Ordine):
    return ordine.model_dump()
