import fitz

def pdf_bytes_to_text(pdf_bytes)->str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    
    return text