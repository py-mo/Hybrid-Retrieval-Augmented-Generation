from utils.filters import filter_segments
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class PreprocessingError(Exception):
    """Custom exception for preprocessing errors"""
    pass

class PreprocessingPipeline:
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the preprocessing pipeline.
        
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

    def process_document(self, text: str) -> Optional[List[str]]:
        """
        Process a single document and return list of filtered text segments.
        
        Args:
            text (str): The input text to process
            
        Returns:
            Optional[List[str]]: List of processed text segments or None if processing fails
            
        Raises:
            PreprocessingError: If the text is invalid or processing fails
            TypeError: If the input is not a string
        """
        try:
            logger.info("Starting document processing")
            
            if not isinstance(text, str):
                logger.error("Invalid input type provided")
                raise TypeError("Input must be a string")
            
            if not text.strip():
                logger.error("Empty or whitespace-only input provided")
                raise PreprocessingError("Input text is empty or whitespace")

            logger.debug("Splitting text into segments")
            segments = text.split(" ")
            if not segments:
                logger.error("Text splitting resulted in no segments")
                raise PreprocessingError("No segments were created after splitting")

            logger.info("Applying filters to segments")
            relevant_segments = filter_segments(segments)
            if not relevant_segments:
                logger.warning("No segments passed the filtering stage")
                return None

            logger.info(f"Successfully processed document. Found {len(relevant_segments)} relevant segments")
            return relevant_segments
            
        except TypeError as e:
            logger.error(f"Type error in document processing: {e}")
            raise
        except PreprocessingError as e:
            logger.error(f"Preprocessing error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in document processing: {e}", exc_info=True)
            raise PreprocessingError(f"Failed to process document: {str(e)}")
