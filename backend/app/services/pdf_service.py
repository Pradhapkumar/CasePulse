"""
PDF Reader Service
Handles PDF file reading and text extraction
"""

import PyPDF2
import os


class PDFReader:
    """Service for reading and extracting text from PDF files"""

    def __init__(self):
        """Initialize PDF reader"""
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def get_pdf_info(self, file_path: str) -> dict:
        """
        Get metadata information from PDF
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with PDF metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return {
                    "pages": len(pdf_reader.pages),
                    "metadata": pdf_reader.metadata
                }
        except Exception as e:
            raise Exception(f"Error reading PDF info: {str(e)}")

    def extract_page_text(self, file_path: str, page_num: int) -> str:
        """
        Extract text from a specific page in PDF
        
        Args:
            file_path: Path to the PDF file
            page_num: Page number (0-indexed)
            
        Returns:
            Text content from the specified page
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if page_num < len(pdf_reader.pages):
                    return pdf_reader.pages[page_num].extract_text()
                else:
                    raise ValueError(f"Page {page_num} does not exist")
        except Exception as e:
            raise Exception(f"Error extracting page text: {str(e)}")
