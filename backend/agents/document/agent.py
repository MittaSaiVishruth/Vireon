import os
import logging
from typing import Dict, Any
from backend.core.interfaces import BaseAgent
from backend.agents.document.parser import PDFParser
from backend.agents.document.chunker import SemanticChunker

logger = logging.getLogger(__name__)

class DocumentAgent(BaseAgent):
    """
    Agent responsible for ingesting a PDF and outputting structured, semantically chunked text.
    """
    def __init__(self):
        self.chunker = SemanticChunker()

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects payload: {"file_path": "/path/to/pdf"}
        Returns: {"chunks": ["chunk1", "chunk2", ...], "metadata": {...}}
        """
        file_path = payload.get("file_path")
        
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at path: {file_path}")
            
        logger.info(f"DocumentAgent starting processing for {file_path}")
        
        # 1. Parse PDF to raw text
        parser = PDFParser(file_path)
        raw_text = parser.parse()
        logger.info(f"Extracted {len(raw_text)} characters from PDF.")
        
        # 2. Semantically Chunk Text
        chunks = self.chunker.chunk(raw_text)
        logger.info(f"Generated {len(chunks)} semantic chunks.")
        
        # 3. Return structured payload
        return {
            "status": "success",
            "file_path": file_path,
            "chunks": chunks,
            "metadata": {
                "num_chunks": len(chunks),
                "original_length": len(raw_text)
            }
        }
