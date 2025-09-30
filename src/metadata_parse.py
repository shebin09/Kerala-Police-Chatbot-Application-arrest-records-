import re
from typing import Dict
import spacy

nlp = spacy.load("en_core_web_sm")

# example regex patterns — adapt after inspecting sample PDFs
FIR_RE = re.compile(r'\b(FIR|Cr\.)\s*[:\-]?\s*([A-Za-z0-9\/\-]+)', re.I)
DATE_RE = re.compile(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})')
SECTION_RE = re.compile(r'u/s\.?\s*([0-9A-Za-z, &\-\(\)]+)', re.I)

def parse_metadata(text: str) -> Dict:
    meta = {"case_no": None, "date": None, "time": None, "place": None, "accused": None, "sections": None}
    # FIR/case number
    m = FIR_RE.search(text)
    if m:
        meta["case_no"] = m.group(2).strip()
    # date
    dm = DATE_RE.search(text)
    if dm:
        meta["date"] = dm.group(1)
    # sections
    sm = SECTION_RE.search(text)
    if sm:
        meta["sections"] = sm.group(1).strip()
    # try NER to get PERSON and GPE
    doc = nlp(text[:2000])  # look at start for header-like info
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    places = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC", "ORG")]
    if persons:
        meta["accused"] = persons[0]
    if places:
        meta["place"] = places[0]
    return meta
