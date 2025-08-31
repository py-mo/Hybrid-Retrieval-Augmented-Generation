from pathlib import Path
import logging
from typing import Optional
from utils import PDFTextExtractor, clean_text

logger = logging.getLogger(__name__)

class TextPreprocessingPipeline:
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the text preprocessing pipeline.
        
        Args:
            log_level (int): Logging level (default: logging.INFO)
        """
        self._configure_logging(log_level)
        
    def _configure_logging(self, log_level: int) -> None:
        """Configure logging with appropriate format and level."""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def process_pdf(self, file_path: str | Path, start_page: Optional[int] = None, end_page: Optional[int] = None) -> Optional[str]:
        """
        Process a PDF file through the complete pipeline:
        1. Extract text from PDF
        2. Clean and normalize the text
        
        Args:
            file_path (str | Path): Path to the PDF file
            start_page (int, optional): First page to extract (1-based indexing)
            end_page (int, optional): Last page to extract (1-based indexing)
            
        Returns:
            Optional[str]: Processed text or None if processing failed
        """
        try:
            logger.info(f"Starting processing pipeline for {file_path}")
            
            extractor = PDFTextExtractor(file_path)
            raw_text = extractor.extract_text(start_page, end_page)
            
            if not raw_text:
                logger.error("Text extraction failed")
                return None
                
            logger.info("Cleaning extracted text")
            processed_text = clean_text(raw_text)
            
            if not processed_text:
                logger.warning("Cleaning resulted in empty text")
                return None
                
            logger.info("Successfully completed text processing pipeline")
            return processed_text
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            return None
