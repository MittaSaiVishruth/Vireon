import fitz  # PyMuPDF
import re
from typing import List

class PDFParser:
    """Extracts raw text from a PDF, performing initial cleaning like removing headers/footers."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> str:
        """Parses the PDF and returns clean, concatenated text."""
        doc = fitz.open(self.file_path)
        text_blocks = []
        
        for page in doc:
            # Extract text
            page_text = page.get_text()
            
            # Basic cleaning: remove newlines that break sentences
            clean_text = page_text.replace("\n", " ")
            
            # Clean up extra spaces
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            text_blocks.append(clean_text)
            
        return " ".join(text_blocks)
