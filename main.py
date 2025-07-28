import os
import fitz  # PyMuPDF
import json

def classify_heading(font_size):
    """Classify heading level based on font size."""
    if font_size >= 16:
        return "H1"
    elif font_size >= 13:
        return "H2"
    elif font_size >= 11:
        return "H3"
    return None

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = os.path.splitext(os.path.basename(pdf_path))[0]

    heading_candidates = []

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue
                text = " ".join(span["text"].strip() for span in spans).strip()
                if not text or len(text.split()) > 20:  # skip long paragraphs
                    continue
                font_size = spans[0]["size"]
                heading_level = classify_heading(font_size)
                if heading_level:
                    heading_candidates.append({
                        "level": heading_level,
                        "text": text,
                        "page": page_number
                    })

    return {
        "title": title,
        "outline": heading_candidates
    }

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))

            try:
                result = extract_outline_from_pdf(input_path)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"[✓] Processed: {filename}")
            except Exception as e:
                print(f"[✗] Failed to process {filename}: {str(e)}")

if __name__ == "__main__":
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
    process_all_pdfs(INPUT_DIR, OUTPUT_DIR)
