from difflib import SequenceMatcher
from modules.section_splitter import extract_sections
from modules.summary_agent import summarize_sections
from PyPDF2 import PdfReader

def extract_text_from_pdf(path):
    with open(path, "rb") as f:
        reader = PdfReader(f)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

def compare_papers(paper_paths):
    comparison = []

    for path in paper_paths:
        text = extract_text_from_pdf(path)
        sections = extract_sections(text)
        summaries = summarize_sections(sections)

        comparison.append({
            "filename": path.split("/")[-1],
            "sections": sections,
            "summaries": summaries
        })

    return comparison

def calculate_similarity(text1, text2):
    return round(SequenceMatcher(None, text1, text2).ratio() * 100, 2)
