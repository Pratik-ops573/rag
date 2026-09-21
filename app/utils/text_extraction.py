from pathlib import Path

import fitz

def extract_text_from_pdf(file_bytes:bytes)-> str:
    """Extract text from pdf"""

    document=fitz.open(stream=file_bytes,filetype="pdf")

    text=""

    for page in document:
        text+=page.get_text()

    document.close()
    return text

def extract_text_from_txt(file_bytes:bytes)-> str:
    """Extract text from txt file"""
    return file_bytes.decode("utf-8")
