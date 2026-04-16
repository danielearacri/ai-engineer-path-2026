from dotenv import load_dotenv
load_dotenv()
import anthropic
import os

# 1. CLIENT
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tool_use_ordine ={
    "name": "estrai_dati_ordine",
    "description": (

        "Estrai i dati strutturati da un ordine di acquisto"
        "Usa questo strumento ogni volta che nel testo è presente un ordine"
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "cliente": {
                "type": "string",
                "description": "Nome del cliente"
            },
            "data_ordine": {
                "type": "string",
                "description": "Data in cui viene emesso l'ordine"
            },
            "prodotto": {
                "type": "string",
                "description": "Nome del prodotto presente nell'ordine"
            },
            "quantita": {
                "type": "number",
                "description": "Quantità del prodotto presente nell'ordine"
            },
            "prezzo_unitario": {
                "type": "number",
                "description": "Prezzo unitario del prodotto presente nell'ordine"
            },
        },
        "required": ["cliente", "data ordine", "prodotto", "quantità", "prezzo unitario"]
    }
}


testo_ordine = """ORDINE DI ACQUISTO N. ORD-2025/089
Data: 10/04/2025
Cliente: Ferramenta Rossi Srl

Articolo richiesto: Trapano elettrico mod. X200
Quantità: 5 pezzi
Prezzo unitario: 89,90 €
Totale ordine: 449,50 €"""

# CHIAMATA API
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[tool_use_ordine],
    messages=[
        {
            "role": "user",
            "content": f"Estrai i dati da questo ordine:\n\n{testo_ordine}"
        }
    ]
)

# LETTURA RISPOSTA
print("stop_reason:", response.stop_reason)

for block in response.content:
    if block.type == "tool_use":
        dati = block.input
        print("\nDati estratti:")
        print(dati)