from io import BytesIO

def text_to_bytes(content:str):
    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    return buffer

def generate_cpp(content,format):
    code_bytes = text_to_bytes(content)
    # Determine the correct extension and mode based on the format
    if "cpp" in format.lower() or "c++" in format.lower():
        filename = "/home/roaim/Desktop/solution.cpp"
    elif "python" in format.lower() or "py" in format.lower():
        filename = "/home/roaim/Desktop/solution.py"
    else:
        filename = "/home/roaim/Desktop/solution.txt"

    with open(filename, "wb") as file:
        file.write(code_bytes.getvalue())

