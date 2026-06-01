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
## 2026-05-30

### Costruito oggi
- Aggiunto logging strutturato in day05/main.py
- logger.info per richiesta in entrata e output Claude
- logger.error per tutti i casi di validazione fallita
- 7/7 test passati

### Prossimo incremento
- Da definire a inizio prossima sessione
- logger.error aggiunto nel blocco except ValueError di pdfplumber (esercizio autonomo)
## 2026-05-31

### Costruito oggi
- Error handling strutturato sulla chiamata Claude API: AuthenticationError (500), RateLimitError (429), APIError (502)
- Try/except su InvoiceData parsing per Pydantic ValidationError (422)
- Import aggiunto: from pydantic import ValidationError
- 7/7 test passati

### Prossimo incremento
- Scrivere test pytest per i nuovi error handler (API errors + ValidationError)
## 2026-05-31

### Costruito oggi
- Test pytest per error handler API: AuthenticationError (500), RateLimitError (429), APIError (502)
- Test pytest per ValidationError Pydantic (422)
- Concetto appreso: side_effect vs return_value nel mock, costruttori diversi per eccezioni SDK Anthropic
- 11/11 test passati

### Prossimo incremento
- Da definire a inizio prossima sessione
## 2026-05-31

### Costruito oggi
- Refactoring client Anthropic da sincrono a asincrono: Anthropic → AsyncAnthropic
- Aggiunto await su client.messages.create() per liberare l'event loop
- Fix test: MagicMock → AsyncMock (new_callable) per i 5 test con return_value
- 11/11 test passati

### Concetti appresi
- Thread: singola sequenza di esecuzione; async event loop = un thread furbo che cede il controllo con await
- Problema sync inside async: chiamata sincrona blocca l'event loop, server non serve altre richieste
- MagicMock non ha __await__, AsyncMock sì: unica differenza tecnica
- side_effect lancia l'eccezi