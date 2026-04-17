from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

pdf.cell(200, 10, txt="FATTURA N. 2026-001", ln=True)
pdf.cell(200, 10, txt="Fornitore: Acme Srl", ln=True)
pdf.cell(200, 10, txt="Partita IVA: 12345678901", ln=True)
pdf.cell(200, 10, txt="Data: 2026-04-17", ln=True)
pdf.cell(200, 10, txt="Totale: EUR 1.250,00", ln=True)

pdf.output("day05/fattura_test.pdf")
print("PDF creato: day05/fattura_test.pdf")