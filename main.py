from db_manager import DatabaseManager, create_document_schema
from pdf_processor import process_pdfs
import os
import logging
from logging.handlers import RotatingFileHandler
import time
import psutil
import json
from datetime import datetime

def setup_logging():
    log_file = 'pdf_processor.log'
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    start_cpu = psutil.cpu_percent()
    start_memory = psutil.virtual_memory().percent

    result = func(*args, **kwargs)

    end_time = time.time()
    end_cpu = psutil.cpu_percent()
    end_memory = psutil.virtual_memory().percent

    performance_metrics = {
        'total_execution_time': end_time - start_time,
        'avg_cpu_usage': (start_cpu + end_cpu) / 2,
        'avg_memory_usage': (start_memory + end_memory) / 2,
        'document_times': {}
    }

    
    for doc in result:
        if 'processing_time' in doc:
            performance_metrics['document_times'][doc['filename']] = doc['processing_time']

    
    if performance_metrics['document_times']:
        performance_metrics['avg_document_time'] = sum(performance_metrics['document_times'].values()) / len(performance_metrics['document_times'])
    else:
        performance_metrics['avg_document_time'] = 0

    return result, performance_metrics

def save_metrics_to_file(results):
    directory = "performance_metrics"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_metrics_{timestamp}.json"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    logging.info(f"Performance metrics saved to {filepath}")

def process_and_store_pdfs(pdf_folder, db_manager):
    processed_docs = process_pdfs(pdf_folder)
    
    for doc in processed_docs:
        existing_doc = db_manager.find_document("documents", {"filename": doc['filename']})
        if existing_doc:
            db_manager.update_document(
                "documents",
                {"filename": doc['filename']},
                {"$set": doc}
            )
        else:
            db_manager.insert_document("documents", doc)
    
    return processed_docs

def main():
    setup_logging()
    logging.info("Starting PDF processing")
    db_manager = DatabaseManager(connection_string='mongodb://localhost:27017')
    try:
        db_manager.connect()
        create_document_schema(db_manager)
        
        pdf_folder = os.path.expanduser("~/Desktop/pdf_folder")
        
        # Using measure_performance to wrap the PDF processing and database operations as of now avoiding the performance_metrics.py
        processed_docs, performance_results = measure_performance(process_and_store_pdfs, pdf_folder, db_manager)
        
        logging.info(f"Processed {len(processed_docs)} documents")
        logging.info(f"Overall performance results: {performance_results}")
        
       

        save_metrics_to_file(performance_results)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()