import pdfplumber
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Riceve un PDF come bytes e restituisce il testo grezzo come stringa.
    Raises ValueError se il PDF è vuoto o non contiene testo estraibile.
    """
    text_parts: list[str] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        if not pdf.pages:
            raise ValueError("PDF privo di pagine")

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())

    if not text_parts:
        raise ValueError("Nessun testo estraibile dal PDF")

    return "\n\n".join(text_parts)