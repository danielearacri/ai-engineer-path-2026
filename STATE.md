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