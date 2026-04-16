from dotenv import load_dotenv
load_dotenv()
import anthropic
import os

# 1. CLIENT
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 2. DEFINIZIONE STRUMENTO (il modulo)
tool_estrai_fattura = {
    "name": "estrai_dati_fattura",
    "description": (
        "Estrai i dati strutturati da una fattura italiana. "
        "Usa questo strumento ogni volta che nel testo è presente una fattura."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "fornitore": {
                "type": "string",
                "description": "Nome o ragione sociale del fornitore"
            },
            "numero_fattura": {
                "type": "string",
                "description": "Numero identificativo della fattura"
            },
            "data_emissione": {
                "type": "string",
                "description": "Data di emissione nel formato GG/MM/AAAA"
            },
            "importo_totale": {
                "type": "number",
                "description": "Importo totale in euro, solo il numero senza simbolo"
            },
            "iva_percentuale": {
                "type": "number",
                 "description": "Percentuale IVA applicata, solo il numero (es. 22 per IVA al 22%)"
            },
        },
        "required": ["fornitore", "numero_fattura", "data_emissione", "importo_totale"]
    }
}

# 3. TESTO FATTURA DI TEST
testo_fattura = """
Spett.le Cliente,

Si emette regolare ricevuta per i servizi resi.
Numero documento: RIC-2025/007
Emesso il: 02/04/2025

Prestatore: Studio Legale Bianchi e Associati

Servizio: Consulenza contrattuale
Compenso netto: 2.500,00 EUR
Rivalsa INPS 4%: 100,00 EUR
IVA 22% su imponibile: 572,00 EUR
Totale documento: 3.172,00 EUR
"""

# 4. CHIAMATA API
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[tool_estrai_fattura],
    messages=[
        {
            "role": "user",
            "content": f"Estrai i dati da questa fattura:\n\n{testo_fattura}"
        }
    ]
)

# 5. LETTURA RISPOSTA
print("stop_reason:", response.stop_reason)

for block in response.content:
    if block.type == "tool_use":
        dati = block.input
        print("\nDati estratti:")
        print(dati)