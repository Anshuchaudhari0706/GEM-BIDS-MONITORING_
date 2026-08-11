import os
import io

"""
PDF Reader & OCR Fallback Module
Extracts text from native PDFs using PyPDF2 / pdfplumber / PyMuPDF (fitz) with OCR fallback.
"""

def extract_text_from_pdf_bytes(pdf_bytes):
    extracted_text = ""
    method_used = "NATIVE_PDF_TEXT"
    ocr_used = False

    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in pdf_reader.pages:
            t = page.extract_text()
            if t:
                extracted_text += t + "\n"
    except Exception as e:
        print(f"PyPDF2 Extraction Notice: {e}")

    # Fallback to pdfplumber if available and text length is small
    if len(extracted_text.strip()) < 50:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        extracted_text += t + "\n"
                method_used = "PDFPLUMBER_TEXT"
        except Exception as e:
            print(f"pdfplumber Extraction Notice: {e}")

    # OCR Fallback if text is still below threshold (Scanned PDF)
    if len(extracted_text.strip()) < 50:
        method_used = "SCANNED_PDF_OCR"
        ocr_used = True
        try:
            import pytesseract
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(pdf_bytes)
            for img in images[:5]: # OCR first 5 pages
                ocr_txt = pytesseract.image_to_string(img)
                if ocr_txt:
                    extracted_text += ocr_txt + "\n"
        except Exception as ocr_err:
            print(f"OCR Reader Notice: {ocr_err}")

    return {
        "text": extracted_text.strip(),
        "method": method_used,
        "ocr_used": ocr_used,
        "length": len(extracted_text.strip())
    }
