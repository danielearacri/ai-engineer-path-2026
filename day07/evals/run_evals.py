import sys
import json
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scorer import score_invoice
from day05.main import extract_invoice_from_bytes

async def main():
    PDF_PATH = Path(__file__).parent/'golden_set'/'synthetic'/'fattura_001.pdf'
    pdf_bytes=open(PDF_PATH, 'rb').read()
    JSON_PATH = Path(__file__).parent/'golden_set'/'synthetic'/'fattura_001.json'
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        expected = json.load(f)
    risultato = await extract_invoice_from_bytes(pdf_bytes)
    actual = risultato.model_dump()
    report = score_invoice(expected, actual)
    print(report)
asyncio.run(main())

