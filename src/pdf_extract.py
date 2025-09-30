import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_text_pdf(pdf_path, ocr_lang="eng", ocr_if_empty=True):
    """Return {'pages': [{'page_no':1,'text':...}], 'full_text': ...}"""
    pdf_path = Path(pdf_path)
    pages_out = []
    full_text_parts = []
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                txt = page.extract_text() or ""
                txt = txt.strip()
                if not txt and ocr_if_empty:
                    # do OCR for this page
                    try:
                        pil = page.to_image(resolution=300).original
                        ocr_txt = pytesseract.image_to_string(pil, lang=ocr_lang)
                        txt = ocr_txt.strip()
                    except Exception as e:
                        logger.debug(f"OCR page {i} failed: {e}")
                pages_out.append({"page_no": i, "text": txt})
                full_text_parts.append(txt)
    except Exception as e:
        # fallback: try full-file image conversion (scanned PDF)
        logger.warning(f"pdfplumber failed for {pdf_path}: {e}; trying convert_from_path OCR.")
        images = convert_from_path(str(pdf_path), dpi=200)
        for i, img in enumerate(images, start=1):
            txt = pytesseract.image_to_string(img, lang=ocr_lang)
            pages_out.append({"page_no": i, "text": txt.strip()})
            full_text_parts.append(txt.strip())

    return {"pages": pages_out, "full_text": "\n".join(full_text_parts)}
