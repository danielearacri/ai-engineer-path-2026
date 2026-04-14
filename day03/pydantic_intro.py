from pydantic import BaseModel
from typing import Optional

class Fattura(BaseModel):
    fornitore: str
    importo: float
    data: str
    note: Optional[str] = None
f = Fattura(fornitore="Acme Srl", importo=1200.0, data="2026-04-10")
print(f)
print(f.model_dump())
