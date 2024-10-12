import logging
from functools import wraps
import traceback

class CustomError(Exception):
    """Base class for custom errors in this module."""
    pass

class PDFProcessingError(CustomError):
    """Raised when there's an error processing a PDF."""
    pass

class DatabaseError(CustomError):
    """Raised when there's a database-related error."""
    pass

def setup_logging(log_file='app.log'):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=log_file,
        filemode='a'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def log_error(error):
    """Log an error with its traceback."""
    logging.error(f"An error occurred: {str(error)}")
    logging.error(traceback.format_exc())

def error_handler(func):
    """Decorator to handle and log errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as e:
            log_error(e)
            raise
        except Exception as e:
            log_error(e)
            raise CustomError(f"An unexpected error occurred in {func.__name__}: {str(e)}")
    return wrapper