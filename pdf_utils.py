import pdfplumber

def load_pdf_pages(file_path: str):
    pages = []

    with pdfplumber.open(file_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "page_number": idx + 1,
                "text": text.strip()
            })

    return pages
