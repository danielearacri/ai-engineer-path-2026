from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()

class FatturaRequest(BaseModel):
    testo: str

@app.post("/estrai-fattura")
async def estrai_fattura(req: FatturaRequest):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Estrai da questo testo: fornitore, importo in euro, data. Rispondi solo in JSON.\n\n{req.testo}"
            }
        ]
    )
    return {"risultato": response.content[0].text}
@app.get("/saluta")
async def saluta(nome: str):
    return f"Ciao {nome}!"
@app.get("/raddoppia")
async def raddoppia(numero: int):
    return {"risultato": numero * 2}
class MoltiplicaRequest(BaseModel):
    numero1:int
    numero2:int
@app.post("/moltiplica")
async def moltiplica(req: MoltiplicaRequest):
    return {"risultato": req.numero1 * req.numero2}