"""
OCR Service
Scanned PDF future support placeholder.
Uses pytesseract + pdf2image for image-based PDFs.
"""

import os
from typing import Optional


class OCRService:
    """
    Future-ready OCR service for scanned/image-based PDFs.
    Currently acts as a placeholder; activate by installing:
        pip install pytesseract pdf2image
    and ensuring Tesseract-OCR is installed on the server.
    """

    OCR_AVAILABLE = False  # Flip to True once dependencies are installed

    def __init__(self):
        if self.OCR_AVAILABLE:
            try:
                import pytesseract
                from pdf2image import convert_from_path
                self._pytesseract = pytesseract
                self._convert = convert_from_path
            except ImportError:
                self.OCR_AVAILABLE = False

    def is_scanned_pdf(self, file_path: str) -> bool:
        """
        Heuristic: if PyPDF2 extracts very little text (<50 chars),
        treat the PDF as a scanned document.
        """
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                total_text = ""
                for page in reader.pages:
                    total_text += page.extract_text() or ""
            return len(total_text.strip()) < 50
        except Exception:
            return False

    def extract_text_via_ocr(self, file_path: str, lang: str = "eng") -> Optional[str]:
        """
        Extract text from a scanned PDF using Tesseract OCR.

        Args:
            file_path : Absolute path to the PDF file.
            lang      : Tesseract language code ('eng', 'hin', 'tam', etc.)

        Returns:
            Extracted text string, or None if OCR is unavailable.
        """
        if not self.OCR_AVAILABLE:
            return (
                "[OCR NOT AVAILABLE] "
                "Install pytesseract + pdf2image and Tesseract-OCR to enable scanned PDF support."
            )

        try:
            pages = self._convert(file_path)
            full_text = ""
            for page_image in pages:
                full_text += self._pytesseract.image_to_string(page_image, lang=lang) + "\n"
            return full_text.strip()
        except Exception as e:
            raise RuntimeError(f"OCR extraction failed: {str(e)}")

    def extract_with_fallback(self, file_path: str) -> str:
        """
        Try normal PDF text extraction first; fall back to OCR if scanned.

        Args:
            file_path: Absolute path to the PDF.

        Returns:
            Best available text from the document.
        """
        if self.is_scanned_pdf(file_path):
            result = self.extract_text_via_ocr(file_path)
            return result or ""

        # Normal text-based PDF — delegate to PDFService
        from app.services.pdf_service import PDFReader
        reader = PDFReader()
        return reader.extract_text(file_path)
