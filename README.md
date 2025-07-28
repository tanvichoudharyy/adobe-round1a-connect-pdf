# Adobe "Connecting the Dots" Challenge – Round 1A

## 🔍 Problem
Extract a structured document outline from PDFs: including Title, H1, H2, and H3 headings, with page numbers.

## 🛠 Approach
We use PyMuPDF to extract font sizes and classify text into heading levels using thresholds. The output is saved as JSON per file.

## 📦 Requirements
- Python 3.10
- Docker (for containerization)

## 🐳 How to Build Docker Image
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
