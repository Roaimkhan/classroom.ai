import fitz
from pprint import pprint

def extract_text_blocks_positions(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = []
    for page in doc:
        text.append(page.get_text("blocks"))

    return text


import io
from PIL import Image
import pymupdf as fitz  # Replaced 'import fitz' to fix the deprecation warning
import pytesseract

import io
import pymupdf  # Replaces deprecated fitz
import pytesseract
from PIL import Image


def extract_pdf_content(pdf_input: str | bytes) -> list[dict]:
    """Extracts text and image OCR content from a PDF, sorted in natural reading order."""
    if isinstance(pdf_input, str):
        doc = pymupdf.open(pdf_input)
    elif isinstance(pdf_input, (bytes, bytearray)):
        doc = pymupdf.open(stream=pdf_input, filetype="pdf")
    else:
        raise TypeError("pdf_input must be a file path (str) or raw PDF bytes")

    parsed_pages = []

    for page_num, page in enumerate(doc, start=1):
        blocks = []

        # 1. Extract text blocks
        for text_block in page.get_text("blocks"):
            x0, y0, x1, y1, text, block_no, block_type = text_block
            cleaned_text = text.strip()
            if cleaned_text:
                blocks.append({
                    "type": "text",
                    "bbox": (x0, y0, x1, y1),
                    "content": cleaned_text,
                })

        # 2. Extract embedded images and OCR
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_obj = Image.open(io.BytesIO(base_image["image"]))

            ocr_text = pytesseract.image_to_string(image_obj).strip()
            if ocr_text:
                rects = page.get_image_rects(xref)
                for rect in rects:
                    blocks.append({
                        "type": "image",
                        "bbox": (rect.x0, rect.y0, rect.x1, rect.y1),
                        "content": ocr_text,
                    })

        # 3. Sort blocks by reading order (Top-to-Bottom, then Left-to-Right)
        # Using round(y0, -1) prevents minor baseline offsets from throwing off line order
        blocks.sort(key=lambda b: (round(b["bbox"][1], -1), b["bbox"][0]))
        parsed_pages.append({"page": page_num, "blocks": blocks})

    doc.close()
    return parsed_pages


def format_as_readable_text(parsed_pages: list) -> str:
    """Formats extracted structured PDF content into clean plain text."""
    output = []

    # Handle cases where parsed_pages might be wrapped or passed improperly
    if isinstance(parsed_pages, dict):
        parsed_pages = [parsed_pages]

    for page in parsed_pages:
        # Guard clause: ensure page is a dictionary
        if not isinstance(page, dict):
            continue

        page_num = page.get("page", "Unknown")
        blocks = page.get("blocks", [])

        output.append(f"--- PAGE {page_num} ---\n")
        for block in blocks:
            if not isinstance(block, dict):
                continue
            
            prefix = "[Image OCR]" if block.get("type") == "image" else ""
            content = block.get("content", "").strip()

            if content:
                if prefix:
                    output.append(f"{prefix}\n{content}\n")
                else:
                    output.append(f"{content}\n")

        output.append("\n")

    return "\n".join(output)

if __name__ == "__main__":
    # Now passing a file path string directly will work without errors
    pdf_path = "/home/roaim/Desktop/projects/gc_agent/agent/2501008_ICT_Assignment 4.pdf"

# Convert to readable Markdown/Text
    data = extract_pdf_content(pdf_path)
    readable_document = format_as_readable_text(data)

    print(readable_document)