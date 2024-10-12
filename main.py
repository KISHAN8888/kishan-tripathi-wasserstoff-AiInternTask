from db_manager import DatabaseManager, create_document_schema
from pdf_processor import process_pdfs
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    db_manager = DatabaseManager(connection_string='mongodb://localhost:27017')
    try:
        db_manager.connect()
        create_document_schema(db_manager)
        
        # Process PDFs
        pdf_folder = os.path.expanduser("~/Desktop/pdf_folder")
        processed_docs = process_pdfs(pdf_folder)
        
        # Insert or update documents in the database
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
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()