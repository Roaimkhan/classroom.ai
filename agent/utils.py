import fitz
from pprint import pprint

def extract_text_blocks_positions(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = []
    for page in doc:
        text.append(page.get_text("blocks"))

    return text


def extract_image_block_position(pdf_bytes):
    doc = fitz.open(pdf_bytes)
    parsed_pages = []

    for page_num, page in enumerate(doc,start=1):

        blocks = []
        for text_block in page.get_text("blocks"):
            x0, y0, x1, y1, text, *_ = text_block
            blocks.append({
                "type":"text",
                "bbox":(x0,y0,x1,y1),
                "content": text,
                })

        for img_block in page.get_images(full=True):
            xref = img_block[0]
            rects = page.get_image_rects(xref)
            for rect in rects:
                blocks.append({
                    "type":"image",
                    "bbox":(rect.x0,rect.y0,rect.x1,rect.y1),
                    "xref": xref,
                })
        
        parsed_pages.append({
            "page":page_num,
            "blocks":blocks
        })

    return parsed_pages
    




if __name__ == "__main__":
    print(extract_image_block_position("/home/roaim/Desktop/projects/gc_agent/agent/2501008_ICT_Assignment 4.pdf"))
    
