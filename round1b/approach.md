## Approach – Adobe Hackathon Round 1B

### Objective
We designed a system that intelligently extracts and ranks relevant sections from a set of PDFs based on the user's persona and their job-to-be-done.

### Step-by-Step:
1. **Persona Understanding:** The persona and job are read from `persona.txt` and `job.txt`.
2. **Text Extraction:** We use PyMuPDF to extract clean paragraph-level text from each PDF.
3. **Semantic Relevance Scoring:** Using a lightweight model (`all-MiniLM-L6-v2`), we convert both the user's context and PDF sections into embeddings and score them via cosine similarity.
4. **Ranking:** The top-ranked sections are included in the output JSON under `sections` and `subsections` based on similarity to the user intent.
5. **Output Format:** Matches the JSON schema required by the challenge.

### Why This Works
- The sentence-transformers model is accurate and fast on CPU.
- The semantic match between the task and content ensures relevance.
- The design is modular and works across personas like students, analysts, or researchers.

### Compliance
- 🧠 Model < 1GB
- 🚀 Runtime < 60s on 5 PDFs
- ✅ Runs offline
- 📦 CPU-only, Docker-ready
