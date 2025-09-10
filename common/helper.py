import fitz

def read_pdf(file_path):
    # read the pdf file using fitz
    return fitz.open(file_path)


def chunk_text(text, chunk_size=500):

    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({"content": chunk.strip()})
        start = end
    
    return chunks

import re

def clean_text(text):

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")    
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\bPage\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b\d+\s*-\s*\d+\b", "", text)

    text = text.strip()
    
    return text