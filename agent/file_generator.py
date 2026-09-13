from io import BytesIO

def generate_py(content:str):
    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    return buffer
