import logging
import re
from pathlib import Path
from typing import List, Optional, Dict
import json
from utils import ( PDFTextExtractor
                , clean_text, filter_segments, Embedder )
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


logger = logging.getLogger(__name__)

class ChunkingPipeline:
    """Pipeline for processing documents into clean, filtered, and embedded chunks."""
    
    def __init__(
        self,
        embedding_model: str = 'sentence-transformers/all-MiniLM-L6-v2',
        model: str = "roberta-base",
        log_level: int = logging.INFO
    ):
        """
        Initialize the chunking pipeline.
        
        Args:
            chunk_size (int): Target size for text chunks in characters
            chunk_overlap (int): Number of characters to overlap between chunks
            embedding_model (str): Name of the sentence-transformer model to use
            model (str): Name of the transformer model to use
            log_level (int): Logging level
        """
        self._configure_logging(log_level)
        self.embedder = Embedder(embedding_model)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSequenceClassification.from_pretrained(model)
        logger.info(f"Initialized ChunkingPipeline with embedding_model={embedding_model}, model={model}")

    def _configure_logging(self, log_level: int) -> None:
        """Configure logging with appropriate format and level."""
        logging.basicConfig(
            level=log_level,
            filename="logs/preprocessing/chunking.log",
            filemode="a",
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _create_chunks(self, text: str) -> List[str]:
        """
        Split text into candidate chunks using RoBERTa.
        Each chunk is scored for relevance
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[str]: List of text chunks
        """
        sentences = re.split(r'(?<=[.!?,])\s+', text)
        logger.info(f"Detected {len(sentences)} sentences for chunking")
        chunks, buffer = [], []

        for sent in sentences:
            buffer.append(sent)
            combined = " ".join(buffer)

            tokens = self.tokenizer(combined, truncation=True, padding=True, return_tensors="pt", max_length=self.tokenizer.model_max_length)
            with torch.no_grad():
                outputs = self.model(**tokens)
                score = torch.softmax(outputs.logits, dim=1)[0][1].item()

            if score > 0.1:
                logger.info(f" combined: {combined}")
                chunks.append(combined)
                buffer = []

        if buffer:
            chunks.append(" ".join(buffer))
        
        chunks.append(combined)

        return chunks
        
    def process_document(self, file_path: Path) -> Dict:
        """
        Process a document through the complete pipeline:
        1. Extract text from PDF
        2. Clean the text
        3. Split into chunks
        4. Filter chunks
        5. Generate embeddings
        
        Args:
            file_path (Path): Path to the PDF document
            
        Returns:
            Dict: Processing results including metadata and chunks
        """
        try:
            extractor = PDFTextExtractor(file_path)
            metadata = extractor.get_pdf_metadata()
            raw_text = extractor.extract_text()
            
            if not raw_text:
                logger.error(f"No text could be extracted from {file_path}")
                return {"error": "Text extraction failed"}
                
            cleaned_text = clean_text(raw_text)
            
            chunks = self._create_chunks(cleaned_text)
            logger.info(f"Created {len(chunks)} initial chunks")
            
            filtered_chunks = filter_segments(chunks)
            logger.info(f"{len(filtered_chunks)} chunks remained after filtering")
            
            chunk_data = []
            for i, chunk in enumerate(filtered_chunks):
                embedding = self.embedder.embed_text(chunk, self.embedder.model)
                chunk_data.append({
                    "id": i,
                    "text": chunk,
                    "embedding": embedding.tolist()
                })
                
            result = {
                "metadata": metadata,
                "chunks": chunk_data,
                "stats": {
                    "initial_chunks": len(chunks),
                    "filtered_chunks": len(filtered_chunks)
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def process_directory(self, dir_path: Path, out_path: Path) -> None:
        """
        Process all PDF files in a directory and save results.
        
        Args:
            dir_path (Path): Path to directory containing PDF files
        """
        try:
            dir_path = Path(dir_path)
            if not dir_path.is_dir():
                raise ValueError(f"Invalid directory path: {dir_path}")
                
            results = []
            for pdf_file in dir_path.glob("*.pdf"):
                logger.info(f"Processing {pdf_file}")
                result = self.process_document(pdf_file)
                if "error" not in result:
                    results.append(result)

            output_path = Path(f"{out_path}/chunks.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2)
                
            logger.info(f"Successfully processed {len(results)} documents")
            
        except Exception as e:
            logger.error(f"Directory processing failed: {str(e)}", exc_info=True)
            raise
