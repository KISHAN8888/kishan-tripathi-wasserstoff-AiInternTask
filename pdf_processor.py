import os
import PyPDF2
from PyPDF2 import PdfReader
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import logging
from keyword_extractor import KeywordExtractor
from summarizer import DynamicSummarizer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_pdfs(folder_path, max_workers=4):
    """
    Process multiple PDFs concurrently from the given folder.
    
    :param folder_path: Path to the folder containing PDFs
    :param max_workers: Maximum number of worker processes
    :return: List of processed document information
    """
    processed_docs = []
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdf = {executor.submit(process_single_pdf, os.path.join(folder_path, pdf)): pdf for pdf in pdf_files}
        for future in as_completed(future_to_pdf):
            pdf = future_to_pdf[future]
            try:
                doc_info = future.result()
                
                processed_docs.append(doc_info)
                logging.info(f"Processed: {pdf}")
            except Exception as e:
                logging.error(f"Error processing {pdf}: {str(e)}")
    
    return processed_docs

def process_single_pdf(file_path):
    """
    Process a single PDF file.
    
    :param file_path: Path to the PDF file
    :return: Dictionary containing document information
    """
    doc_info = extract_pdf_info(file_path)
    doc_info['content'] = extract_pdf_content(file_path)
    doc_info['length_category'] = classify_document_length(doc_info['num_pages'])
    paragraphs = extract_paragraphs_with_boundaries(file_path)
    doc_info['final_paragraphs'] = merge_short_paragraphs(paragraphs)
    doc_info['summary'] = summarize(doc_info, file_path)
    doc_info['keywords'] = extract_keywords(doc_info)
    
    return doc_info

def extract_pdf_info(file_path):
    """
    Extract metadata from a PDF file.
    
    :param file_path: Path to the PDF file
    :return: Dictionary containing PDF metadata
    """
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        metadata = reader.metadata
        
    file_info = os.stat(file_path)
    file_size = file_info.st_size
    creation_time = file_info.st_ctime
    
    return {
        'filename': os.path.basename(file_path),
        'path': file_path,
        'num_pages': num_pages,
        'author': metadata.get('/Author', 'Unknown'),
        'creation_date': metadata.get('/CreationDate', 'Unknown'),
        'file_size': file_size,
        'system_creation_date': datetime.fromtimestamp(creation_time).isoformat(),
        'processing_status': 'processed',
        'last_updated': datetime.now().isoformat()
    }

def extract_pdf_content(file_path):
    """
    Extract text content from a PDF file.
    
    :param file_path: Path to the PDF file
    :return: Extracted text content
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if reader.is_encrypted:
                return handle_encrypted_pdf(file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return content
    except PyPDF2.errors.PdfReadError as e:
        logging.error(f"Error reading PDF {file_path}: {str(e)}")
        return ""

def extract_paragraphs_with_boundaries(file_path):
    reader = PdfReader(file_path)
    if reader.is_encrypted:
        return handle_encrypted_pdf(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    paragraphs = re.split(r'\n\s*\n', text.strip())
    paragraph_info = []
    current_position = 0

    for para_index, paragraph in enumerate(paragraphs):
        paragraph_start = current_position
        paragraph_end = paragraph_start + len(paragraph)
        current_position = paragraph_end + 2
        
        paragraph_info.append({
            'paragraph_index': para_index + 1,
            'paragraph_start': paragraph_start,
            'paragraph_end': paragraph_end,
            'paragraph_text': paragraph
        })

    return paragraph_info

def merge_short_paragraphs(paragraphs, word_threshold=150):
    merged_paragraphs = []
    temp_paragraph = ""
    
    for i, para_info in enumerate(paragraphs):
        paragraph = para_info['paragraph_text']
        word_count = len(paragraph.split())

        if word_count < word_threshold:
            if temp_paragraph:
                temp_paragraph += " " + paragraph
            else:
                temp_paragraph = paragraph
        else:
            if temp_paragraph:
                merged_paragraphs.append(temp_paragraph + " " + paragraph)
                temp_paragraph = ""
            else:
                merged_paragraphs.append(paragraph)

    if temp_paragraph:
        merged_paragraphs.append(temp_paragraph)

    return merged_paragraphs

def classify_document_length(num_pages):
    """
    Classify the document length based on the number of pages.
    """
    try:
        num_pages = int(num_pages)  # Ensure num_pages is an integer
        if num_pages <= 2:
            return "short"
        elif num_pages <= 12:
            return "medium"
        else:
            return "long"
    except ValueError:
        logging.error(f"Invalid number of pages: {num_pages}")
        return "unknown"

def handle_encrypted_pdf(file_path):
    """
    Handle encrypted PDF files.
    
    :param file_path: Path to the encrypted PDF file
    :return: A message indicating the file is encrypted
    """
    logging.warning(f"Encrypted PDF detected: {file_path}")
    return "This PDF is encrypted and cannot be processed without a password."

def extract_keywords(doc_info):
    """
    Extract keywords from the document content.
    
    :param doc_info: Dictionary containing document information
    :return: List of extracted keywords
    """
    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(doc_info['content'], num_keywords=10)
    return keywords  # Return only the keywords list

def summarize(doc_info, file_path):
    """
    Summarize the document content.
    
    :param doc_info: Dictionary containing document information
    :param file_path: Path to the PDF file
    :return: String containing the document summary
    """
    summarizer = DynamicSummarizer()
    summary = summarizer.summarize_document(doc_info['final_paragraphs'], file_path)
    
    logging.info(f"Summary for {doc_info['filename']}: {summary}")
    
    return summary  # Return only the summary string


if __name__ == "__main__":
    folder_path = "C:\\Users\\kisha\\Desktop\\pdf_folder"
    processed_docs = process_pdfs(folder_path)
    for doc in processed_docs:
        print(f"Processed: {doc['filename']}")
        print(f"Number of pages: {doc['num_pages']}")
        print(f"Keywords: {doc['keywords']}")
        print(f"Summary:{doc['summary']})")
        print("---")
