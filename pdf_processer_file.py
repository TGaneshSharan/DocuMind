import pymupdf


def extract_text_from_pdf(pdf_path):

    extracted_pages = []

    with pymupdf.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text()

            extracted_pages.append({
                "page_number": page_number,
                "text": text
            })

    return extracted_pages