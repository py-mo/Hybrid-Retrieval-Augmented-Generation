from pathlib import Path
from typing import Optional, Dict, List
import logging
import pypdf
from datetime import datetime


logger = logging.getLogger(__name__)


class PDFTextExtractor:
    
    def __init__(self, file_path: Path, log_level: int = logging.INFO):
        """
        Initialize the PDF text extractor.
        
        Args:
            file_path (Path): Path to the PDF file
            log_level (int): Logging level (default: logging.INFO)
        
        Raises:
            ValueError: If the file path is invalid or not a PDF
        """
        self._configure_logging(log_level)
        self.file_path = self._validate_file_path(file_path)
        logger.info(f"Initialized PDFTextExtractor for {self.file_path}")
        
    def _configure_logging(self, log_level: int) -> None:
        """Configure logging with appropriate format and level."""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _validate_file_path(self, file_path: Path) -> Path:
        """
        Validate the provided file path.
        
        Raises:
            ValueError: If the file doesn't exist or isn't a PDF
        """
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
            
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise ValueError(f"File does not exist: {file_path}")
            
        if file_path.suffix.lower() != ".pdf":
            logger.error(f"Invalid file type: {file_path.suffix}")
            raise ValueError(f"File is not a PDF: {file_path}")
            
        return file_path
    
    def get_pdf_metadata(self) -> Dict:
        """
        Extract metadata from the PDF file.
        
        Returns:
            Dict: PDF metadata including creation date, number of pages, etc.
        """
        try:
            with open(self.file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                metadata = {
                    'number_of_pages': len(reader.pages),
                    'encrypted': reader.is_encrypted,
                    'metadata': reader.metadata if reader.metadata else {},
                    'file_size': self.file_path.stat().st_size,
                    'extraction_time': datetime.now().isoformat()
                }
            logger.debug(f"Successfully extracted metadata from {self.file_path}")
            return metadata
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}", exc_info=True)
            return {}

    def extract_text(self, start_page: int = None, end_page: int = None) -> Optional[str]:
        """
        Extract text from the PDF file with optional page range.
        
        Args:
            start_page (int, optional): First page to extract (1-based indexing)
            end_page (int, optional): Last page to extract (1-based indexing)
            
        Returns:
            Optional[str]: Extracted text or None if extraction failed
        """
        try:
            logger.info(f"Starting text extraction from {self.file_path}")
            with open(self.file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                total_pages = len(reader.pages)
                
                start_page = max(1, start_page or 1) - 1
                end_page = min(end_page or total_pages, total_pages)
                
                if start_page >= end_page:
                    logger.error("Invalid page range specified")
                    raise ValueError("Invalid page range")
                
                text: List[str] = []
                for page_num in range(start_page, end_page):
                    logger.debug(f"Processing page {page_num + 1}/{total_pages}")
                    content = reader.pages[page_num].extract_text()
                    if content:
                        text.append(content.strip())
                    else:
                        logger.warning(f"No text content found on page {page_num + 1}")
                
                result = "\n\n".join(text)
                if not result:
                    logger.warning("No text content found in document")
                    return "Nothing Found"
                    
                logger.info(f"Successfully extracted {len(text)} pages of text")
                return result
                
        except Exception as e:
            logger.error(f"Failed to extract text from {self.file_path}: {e}", exc_info=True)
            return None


if __name__ == "__main__":
    logging.basicConfig(filename="logs/utils/extraction.log", filemode="a", level=logging.INFO)
    pdf_extractor = PDFTextExtractor("data/2407.00553v1.pdf")
    print(pdf_extractor.get_pdf_metadata())
