import fitz  # PyMuPDF
import os
import copy
import json

skip_pages = 10
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # Start at the current file's directory
print(f"Project root: {project_root}")

# Construct PDF path
pdf_path = os.path.join(project_root, "data", "input", "recipe-book.pdf")


def is_numeric(text):
    try:
        float(text)
        return True
    except ValueError:
        return False
    
def sort_spans(doc, skip_pages=0):
    all_spans = []
    for page_num, page in enumerate(doc[skip_pages:], start=skip_pages+1):
        spans = []

        # Collect all spans from all blocks
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        span["page"] = page_num
                        spans.append(span)

        # Sort spans by y (top of bbox), then x (left of bbox)
        spans_sorted = sorted(spans, key=lambda s: (round(s["bbox"][1], 1), s["bbox"][0]))
        all_spans.extend(spans_sorted)

    return all_spans

def semantic_chunking(spans):
    chunks = []
    new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}
    new_recipe = False
    for span in spans:

        if span["font"] == "MarkerFelt" and int(span["size"]) == 23.0:  # Only add non-empty spans
            if not new_recipe:
                #print(new_recipe_data)
                if new_recipe_data["name"] or new_recipe_data["content"]:
                    new_recipe_data["metadata"]["page"] = span["page"]
                    chunks.append(copy.deepcopy(new_recipe_data))
                new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}

            new_recipe = True
            new_recipe_data["name"] += " " + span["text"].strip()

        else:
            new_recipe = False
            if int(span['size']) == 20.0 and is_numeric(span["text"]):
                continue
            if int(span["size"]) == 12.0 and span["text"].strip() == "page":
                continue
            if int(span["size"]) != 30.0:
                new_recipe_data["content"] += span["text"].strip() + " "

    return chunks

def semantic_cunks_unsorted(doc, skip_pages=0):
    spans = []
    new_recipe = False
    new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}

    for page_num, page in enumerate(doc[skip_pages:], start=skip_pages):

            # Collect all spans from all blocks
            for b in page.get_text("dict")["blocks"]:
                if "lines" in b:
                    for line in b["lines"]:
                        for span in line["spans"]:
                            span["page"] = page_num
                            if span["font"] == "MarkerFelt" and int(span["size"]) == 23.0:  # Only add non-empty spans
                                if not new_recipe:
                                    #print(new_recipe_data)
                                    if new_recipe_data["name"] or new_recipe_data["content"]:
                                        new_recipe_data["metadata"]["page"] = page_num
                                        spans.append(copy.deepcopy(new_recipe_data))
                                    new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}

                                new_recipe = True
                                new_recipe_data["name"] += " " + span["text"].strip()

                            else:
                                new_recipe = False
                                if int(span['size']) == 20.0 and is_numeric(span["text"]):
                                    continue
                                if int(span["size"]) == 12.0 and span["text"].strip() == "page":
                                    continue
                                if int(span["size"]) != 30.0:
                                    new_recipe_data["content"] += span["text"].strip() + " "
    
    return spans



doc = fitz.open(pdf_path)

#unsorted_spans_chunks = semantic_cunks_unsorted(doc, skip_pages=skip_pages)
#with open("unsorted_spans_chunks.json", "w", encoding="utf-8") as f:
#    json.dump(unsorted_spans_chunks, f, ensure_ascii=False, indent=4)
#
#all_sorted_spans = sort_spans(doc, skip_pages=skip_pages)
#sorted_span_chunks = semantic_chunking(all_sorted_spans)
#with open("sorted_span_chunks.json", "w", encoding="utf-8") as f:
#    json.dump(sorted_span_chunks, f, ensure_ascii=False, indent=4)
#
#with open("all_sorted_spans.json", "w", encoding="utf-8") as f:
#    json.dump(all_sorted_spans, f, ensure_ascii=False, indent=4)

import pdfplumber

def extract_pdf_text(pdf_path, skip_pages=0):
    """Extract text from PDF using pdfplumber, page by page."""
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages[skip_pages:], start=skip_pages + 1):

            text = page.extract_text(x_tolerance=2, y_tolerance=2)  # tweak tolerances for column alignment
            if text:
                full_text += f"\n--- Page {page_num} ---\n{text}"
    
    return full_text


all_text = extract_pdf_text(pdf_path)
with open("plumber_extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)