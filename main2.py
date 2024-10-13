import logging
from logging.handlers import RotatingFileHandler
from db_manager import DatabaseManager, create_document_schema
from testpdfprocessor import process_pdfs
from performance_metrics import measure_performance
import os

def setup_logging():
    log_file = 'pdf_processor.log'
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def main():
    setup_logging()
    logging.info("Starting PDF processing")

    db_manager = DatabaseManager(connection_string='mongodb://localhost:27017')
    try:
        db_manager.connect()
        create_document_schema(db_manager)
        
        pdf_folder = os.path.expanduser("~/Desktop/pdf_folder")
        
        # Process PDFs with performance metrics
        max_workers = 1 # Set the fixed number of workers here
        results = measure_performance(process_pdfs, max_workers, pdf_folder)
        
        # Store processed documents into the database
        for doc in results['document_times'].keys():
            doc_info = {
                'filename': doc,
                'processing_time': results['document_times'][doc]
            }
            existing_doc = db_manager.find_document("documents", {"filename": doc})
            if existing_doc:
                db_manager.update_document(
                    "documents",
                    {"filename": doc},
                    {"$set": doc_info}
                )
            else:
                db_manager.insert_document("documents", doc_info)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        db_manager.close()
        logging.info("PDF processing completed")

if __name__ == "__main__":
    main()
