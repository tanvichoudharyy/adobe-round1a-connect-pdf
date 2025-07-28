import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

def load_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if text and len(text.split()) > 5:
                sections.append({
                    "text": text,
                    "page": page_number
                })
    return sections

def load_context(input_dir):
    with open(os.path.join(input_dir, "persona.txt"), "r", encoding="utf-8") as f:
        persona = f.read().strip()
    with open(os.path.join(input_dir, "job.txt"), "r", encoding="utf-8") as f:
        job = f.read().strip()
    return persona, job

def extract(input_dir):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    persona, job = load_context(input_dir)
    query_embedding = model.encode(f"{persona} {job}", convert_to_tensor=True)

    sections = []
    file_list = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

    for pdf_file in file_list:
        doc_sections = load_text_from_pdf(os.path.join(input_dir, pdf_file))
        for section in doc_sections:
            section["document"] = pdf_file
        sections.extend(doc_sections)

    section_texts = [s["text"] for s in sections]
    section_embeddings = model.encode(section_texts, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, section_embeddings)[0].cpu().tolist()

    for i, sim in enumerate(similarities):
        sections[i]["score"] = sim

    # Sort and select top N
    top_sections = sorted(sections, key=lambda x: -x["score"])[:5]

    output = {
        "metadata": {
            "documents": file_list,
            "persona": persona,
            "job": job,
            "processed_at": datetime.utcnow().isoformat() + "Z"
        },
        "sections": [],
        "subsections": []
    }

    for rank, section in enumerate(top_sections, start=1):
        output["sections"].append({
            "document": section["document"],
            "page": section["page"],
            "title": section["text"][:80],  # crude title
            "importance_rank": rank
        })
        output["subsections"].append({
            "document": section["document"],
            "page": section["page"],
            "refined_text": section["text"],
            "importance_rank": rank
        })

    return output

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    output_path = os.path.join(output_dir, "output.json")

    result = extract(input_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
