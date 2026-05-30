## 2026-05-29

### Costruito oggi
- Riletto i 4 strati della pipeline (FastAPI, pdfplumber, Claude tool use, Pydantic)

### Prossimo incremento
- Aggiungere validazione di merito in day05/main.py: total_amount > 0, vat_number 11 cifre
## 2026-05-29

### Costruito oggi
- Riletto i 4 strati della pipeline (FastAPI, pdfplumber, Claude tool use, Pydantic)
- Aggiunta validazione di merito in day05/main.py: total_amount > 0, vat_number 11 cifre numeriche

### Prossimo incremento
- Aggiungere test pytest per i nuovi controlli di merito (total_amount <= 0, vat_number malformato)
## 2026-05-29

### Costruito oggi
- Riletto i 4 strati della pipeline (FastAPI, pdfplumber, Claude tool use, Pydantic)
- Aggiunta validazione di merito in day05/main.py: total_amount > 0, vat_number 11 cifre numeriche
- Scritti test pytest con mock per i due nuovi controlli: 4/5 test passano

### Prossimo incremento
- Fixare test_extract_pdf_successo: API KEY disattivata
 Incremento successivo: aggiungere validazione su invoice_date (formato ISO 8601)
 ## 2026-05-30

### Costruito oggi
- Fix PDF_PATH con pathlib in test_extract.py: percorso assoluto indipendente da dove si lancia pytest
- Validazione invoice_date: formato ISO 8601 con date.fromisoformat()
- Validazione invoice_number: non vuoto con .strip()
- Test 7/7 passati

### Prossimo incremento
- Da definire a inizio prossima sessione