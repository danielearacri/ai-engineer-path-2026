import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import asyncio
from pathlib import Path
from day05.main import extract_invoice_from_bytes

async def main():
    PDF_PATH = Path(__file__).parent/'golden_set'/'synthetic'/'fattura_001.pdf'
    pdf_bytes=open(PDF_PATH, 'rb').read()
    risultato = await extract_invoice_from_bytes(pdf_bytes)
    print(risultato.model_dump())
asyncio.run(main())
