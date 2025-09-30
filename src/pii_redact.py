import re
import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

AADHAAR_RE = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
MOBILE_RE = re.compile(r'\b[6-9]\d{9}\b')
EMAIL_RE = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.\w{2,}\b')
PAN_RE = re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b')

def find_spans(text: str) -> List[Dict]:
    spans = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "GPE", "ORG", "DATE"):
            spans.append({"start": ent.start_char, "end": ent.end_char, "label": ent.label_, "text": ent.text})
    for patt, label in [(AADHAAR_RE, "AADHAAR"), (MOBILE_RE, "MOBILE"), (EMAIL_RE, "EMAIL"), (PAN_RE, "PAN")]:
        for m in patt.finditer(text):
            spans.append({"start": m.start(), "end": m.end(), "label": label, "text": m.group(0)})
    spans = sorted({(s['start'], s['end']): s for s in spans}.values(), key=lambda x: x['start'])
    return spans

def redact(text: str, spans: List[Dict]) -> str:
    if not spans:
        return text
    parts = []
    last = 0
    for s in spans:
        parts.append(text[last:s['start']])
        parts.append(f"[{s['label']}]")
        last = s['end']
    parts.append(text[last:])
    return "".join(parts)
