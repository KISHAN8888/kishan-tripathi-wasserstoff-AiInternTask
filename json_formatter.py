import json
from datetime import datetime

class JSONFormatter:
    @staticmethod
    def format_document(doc_info):
        formatted_doc = {
            "filename": doc_info['filename'],
            "path": doc_info['path'],
            "metadata": {
                "num_pages": doc_info['num_pages'],
                "author": doc_info['author'],
                "creation_date": doc_info['creation_date'],
                "file_size": doc_info['file_size']
            },
            "processing": {
                "status": doc_info['processing_status'],
                "last_updated": doc_info['last_updated']
            },
            "content": {
                "summary": doc_info.get('summary', ''),
                "keywords": doc_info.get('keywords', [])
            }
        }
        
        return