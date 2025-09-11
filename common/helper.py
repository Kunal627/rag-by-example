import fitz
import copy
import re

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



def clean_text(text):

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")    
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\bPage\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b\d+\s*-\s*\d+\b", "", text)

    text = text.strip()
    
    return text



def extract_recipes_from_pdf(doc, skip_pages=10, end_page=62):

    new_recipe = False
    new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}
    spans = []
    directions = ""
    ingredients = ""
    for page_num, page in enumerate(doc[skip_pages:end_page], start=skip_pages+1):
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        if span["font"] == "MarkerFelt" and int(span["size"]) == 23.0:
                            if not new_recipe:
                                if new_recipe_data["name"] or new_recipe_data["content"]:
                                    new_recipe_data["metadata"]["page"] = page_num
                                    new_recipe_data["content"] = directions.strip() + "\nIngredients:" + ingredients.strip()
                                    spans.append(copy.deepcopy(new_recipe_data))
                                new_recipe_data = {"name": "", "content": "", "metadata": {"page": 0}}
                                directions = ""
                                ingredients = ""
                            new_recipe = True
                            new_recipe_data["name"] += " " + span["text"].strip()

                        else:
                            if span["color"] == 16777215 and span["char_flags"] == 24: # white text
                                ingredients += " " + span["text"].strip().replace("\n", " ") + ","
                            #if is_numeric(span["text"]):
                            #    continue

                            if span['font'] in ['OpenSans-SemiboldItalic', 'OpenSans-Light'] and span['char_flags'] in [16, 24] and span['color'] !=16777215:
                                directions += " " + span["text"].strip() 
                            new_recipe = False
    return spans
                    

def is_numeric(text):
    try:
        float(text)
        return True
    except ValueError:
        return False
