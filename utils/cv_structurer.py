"""
CV Structurer Utility

Attempts to structure raw CV text into sections: Name, Contact, Experience, Skills, Education, Languages, etc.
"""
import re

def structure_cv_text(cv_text: str) -> str:
    """Structure the CV text into labeled sections for LLM input."""
    sections = {
        'Name': '',
        'Contact': '',
        'Experience': '',
        'Skills': '',
        'Education': '',
        'Languages': '',
        'Other': ''
    }
    # Simple heuristics for section extraction
    lines = cv_text.splitlines()
    current_section = 'Other'
    for line in lines:
        l = line.strip()
        if not l:
            continue
        if re.search(r'^(Name|Contact|Experience|Skills|Education|Languages)', l, re.I):
            for sec in sections:
                if l.lower().startswith(sec.lower()):
                    current_section = sec
                    break
        sections[current_section] += l + '\n'
    # Build CSV-like block
    structured = ''
    for sec, content in sections.items():
        if content.strip():
            structured += f'{sec}: {content.strip()}\n'
    return structured.strip() 