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
- side_effect lancia l'eccezione


## 2026-06-01

### Costruito oggi

- Decisione: Prossimo incremento= eval, piu lungo ma piu utile
- Buildato la cartella day07\evals con tutte le sottocartelle che ci serviranno (golden_set/real and synthetic, README.md, results)
-README golden_set scritto: razionale vs reale, tre ruoli (claude, reportlab, me), piano sub

### Concetti appresi

- req.txt: pip freeze scrive il file, pip install -r lo legge
- Markdown base- spazio dopo # e righe vuote tra le sezioni

### Prossimo incremento

-implementa generate_synthetic.py: generare prima fattura PDF sintetica ita
## 2026-06-01 (sessione 2)

### Costruito oggi
- Implementato day07/evals/generate_synthetic.py
- Schema tool use INVOICE_TOOL con 6 campi: invoice_number, invoice_date, vat_number, customer_name, line_items (array di oggetti annidati), total_amount
- Funzione generate_invoice_data(): chiamata Claude con tool_choice forzato, ritorna dict
- Funzione render_pdf(): SimpleDocTemplate A4 con margini 2cm, Paragraph per intestazione e dati, Table con TableStyle (header grigio, importi allineati a destra)
- Generato fattura_001.pdf nella cartella golden_set/synthetic
- Scritta golden_set/synthetic/fattura_001.json a mano leggendo dal PDF (NON copiata dall'output di Claude)
- JSON validato con json.load(): OK

### Concetti appresi
- Pattern reportlab platypus: crei oggetti (Paragraph, Spacer, Table), li aggiungi a una lista story, alla fine doc.build(story) scrive il file
- Sistema di coordinate Table: (colonna, riga), -1 = ultimo; rettangolo definito da due coordinate estremi inclusi
- Tag inline reportlab (<b>, <i>) interpretati da Paragraph, NON HTML vero
- F-string con formattatore: f"{numero:.2f}" forza due decimali fissi
- Differenza inline vs variabile intermedia: usi variabile solo quando devi configurare l'oggetto post-creazione (es. Table.setStyle)
- Indipendenza della golden label: se la prendessi dall'output di Claude, valuterei Claude contro sé stesso, eval inutili. La verità deve venire da fonte esterna al sistema valutato
- JSON strict: niente trailing comma, niente unità (€) dentro numeri, stringhe con doppi apici

### Prossimo incremento
- Implementare scorer.py: confronta output pipeline day05 vs golden label, ritorna metriche (campo-per-campo match, accuracy totale)
- Prima incremento più piccolo: scrivere run_evals.py che carica il PDF sintetico, lo passa a pipeline day05, restituisce il dict estratto