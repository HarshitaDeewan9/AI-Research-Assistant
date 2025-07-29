def extract_sections(text):
    sections = {"Abstract": "", "Methodology": "", "Results": "", "Conclusion": ""}
    lower = text.lower()
    for sec in sections.keys():
        if sec.lower() in lower:
            start = lower.find(sec.lower())
            end = lower.find("\n", start + len(sec)) + 500
            sections[sec] = text[start:end]
    return sections