import re
from typing import List
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from backend.core.config import settings

class SemanticChunker:
    """Chunks text into semantically cohesive blocks using sentence embeddings."""
    
    def __init__(self, threshold: float = 0.55):
        self.threshold = threshold
        # Initialize embedding model (downloads locally if not present)
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def _split_into_sentences(self, text: str) -> List[str]:
        """Splits raw text into sentences."""
        # Regex to split on sentence endings (.!?) not preceded by abbreviations
        sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
        sentences = [s.strip() for s in sentence_endings.split(text) if s.strip()]
        return sentences

    def chunk(self, text: str) -> List[str]:
        """Groups sentences into semantic chunks based on embedding cosine similarity."""
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            return []
            
        if len(sentences) == 1:
            return sentences

        embeddings = self.model.encode(sentences)
        
        segments = []
        current_chunk = [sentences[0]]
        
        for i in range(len(sentences) - 1):
            # Compare current sentence to the next sentence
            sim = cosine_similarity(
                embeddings[i].reshape(1, -1), 
                embeddings[i+1].reshape(1, -1)
            )[0][0]
            
            if sim < self.threshold:
                # If similarity is below threshold, break the chunk
                segments.append(" ".join(current_chunk))
                current_chunk = [sentences[i+1]]
            else:
                # Otherwise, continue the chunk
                current_chunk.append(sentences[i+1])
                
        # Append the last chunk
        if current_chunk:
            segments.append(" ".join(current_chunk))
            
        return segments
