import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

load_dotenv()
client = Anthropic()
INVOICE_TOOL = {
    "name": "submit_invoice",
    "description": "Genera i dati di una fattura italiana plausibile per testing.",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_number": {
                "type": "string",
                "description": "Numero progressivo formato AAAA/NNNN, es 2026/0142"
            },
            "invoice_date": {
                "type": "string",
                "description": "ISO 8601, YYYY-MM-DD"
            },
            "vat_number": {
                "type": "string",
                "description": "Partita IVA italiana, 11 cifre numeriche"
            },
            "customer_name": {
                "type": "string",
                "description": "Nome del cliente"
            },
            "line_items": {
                "type": "array",
                "description": "Array di oggetti con description (string) e amount (number)",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Descrizione del prodotto o servizio"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Importo del prodotto o servizio"
                        }
                    },
                    "required": ["description", "amount"]
                }
            },

            "total_amount": {
                "type": "number",
                "description": "Importo totale in euro"
            }
            
        },
        "required": ["invoice_number", "invoice_date", "vat_number", 
                     "customer_name", "line_items", "total_amount"]
    }
}
def generate_invoice_data() -> dict:
    """Chiama Claude e ritorna un dict con i dati della fattura."""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=[INVOICE_TOOL],
        tool_choice={"type": "tool", "name": "submit_invoice"},
        messages=[{
            "role": "user",
            "content": "Genera i dati di una fattura italiana plausibile. Una sola fattura, 2-4 righe, importi realistici per servizi di consulenza IT."
        }]
    )

    for block in response.content:
        if block.type == "tool_use":
            return block.input
    
    raise ValueError("Claude non ha usato il tool")
def render_pdf(data: dict, output_path: str) -> None:
    """Impagina i dati della fattura in un PDF e salva su disco"""
    doc=SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,      
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph('FATTURA', styles['Title']))
    story.append(Spacer(1, 12))
    # Dati fattura
    story.append(Paragraph(f"<b>Numero:</b> {data['invoice_number']}", styles['Normal']))
    story.append(Paragraph(f"<b>Data:</b> {data['invoice_date']}", styles['Normal']))
    story.append(Spacer(1, 12))
    # Dati cliente
    story.append(Paragraph(f"<b>Cliente:</b> {data['customer_name']}", styles['Normal']))
    story.append(Paragraph(f"<b>Partita IVA:</b> {data['vat_number']}", styles['Normal']))
    story.append(Spacer(1, 24))


    table_data= [['Descrizione', 'Importo']]
    for item in data['line_items']:
        table_data.append([item['description'], f"{item['amount']:.2f} €"])
        
    table = Table(table_data, colWidths=[12*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(table)
    # Totale
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"<b>TOTALE: {data['total_amount']:.2f} €</b>",
        styles['Heading2']
    ))
    # Build del PDF
    doc.build(story)
if __name__ == "__main__":
    data = generate_invoice_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    output_path = "day07/evals/golden_set/synthetic/fattura_001.pdf"
    render_pdf(data, output_path)
    print(f"\nPDF salvato: {output_path}")