# Domain-Specific PDF Summarization & Keyword Extraction Pipeline

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Key Components](#key-components)
   3.1 [Main Script (main.py)](#main-script-mainpy)
   3.2 [PDF Processor (pdf_processor.py)](#pdf-processor-pdf_processorpy)
   3.3 [Summarizer (summarizer.py)](#summarizer-summarizerpy)
   3.4 [Keyword Extractor (keyword_extractor.py)](#keyword-extractor-keyword_extractorpy)
   3.5 [Database Manager (db_manager.py)](#database-manager-db_managerpy)
   3.6 [Performance Metrics (performance_metrics.py)](#performance-metrics-performance_metricspy)
   3.7 [Utilities (utils.py)](#utilities-utilspy)
4. [Installation and Setup](#installation-and-setup)
5. [Usage Instructions](#usage-instructions)
6. [Performance Considerations](#performance-considerations)
7. [Error Handling and Logging](#error-handling-and-logging)
8. [Future Enhancements](#future-enhancements)

## 1. Project Overview

The Domain-Specific PDF Summarization & Keyword Extraction Pipeline is a sophisticated system designed to process PDF documents, extract key information, generate summaries, and identify relevant keywords. This pipeline is particularly useful for organizations dealing with large volumes of domain-specific documents, such as research papers, technical reports, or legal documents.

Key features of the pipeline include:
- Multi-threaded PDF processing for improved performance
- Dynamic summarization based on document length and content
- Intelligent keyword extraction using TF-IDF and frequency analysis
- Integration with a MongoDB database for storing processed document information
- Performance monitoring and metrics collection

## 2. System Architecture

The pipeline follows a modular architecture, with each component responsible for a specific task in the document processing workflow. Here's a high-level overview of the system architecture:

1. **Main Script**: Orchestrates the entire pipeline, managing the flow of documents through various processing stages.
2. **PDF Processor**: Handles the extraction of text and metadata from PDF files.
3. **Summarizer**: Generates concise summaries of the extracted text using advanced NLP techniques.
4. **Keyword Extractor**: Identifies and extracts relevant keywords from the document content.
5. **Database Manager**: Manages interactions with the MongoDB database for storing and retrieving document information.
6. **Performance Metrics**: Monitors and records various performance metrics throughout the processing pipeline.
7. **Utilities**: Provides common utility functions used across different components of the pipeline.

## 3. Key Components

### 3.1 Main Script (main.py)

The main script serves as the entry point for the pipeline and coordinates the overall document processing workflow. Key responsibilities include:

- Setting up logging
- Initializing the database connection
- Processing PDFs in the specified folder
- Coordinating the extraction of information, summarization, and keyword identification
- Storing processed document information in the database

### 3.2 PDF Processor (pdf_processor.py)

The PDF Processor is responsible for handling PDF files and extracting relevant information. Main features include:

- Multi-threaded processing of PDF files using `ProcessPoolExecutor`
- Extraction of metadata (e.g., filename, number of pages, author, creation date)
- Text extraction from PDF content
- Handling of encrypted PDFs
- Classification of document length (short, medium, long)

### 3.3 Summarizer (summarizer.py)

The Summarizer component generates concise summaries of the extracted text using advanced NLP techniques. Key features include:

- Dynamic summarization based on document length
- Extraction of key sentences using TF-IDF scoring
- Integration with the Groq LLM (Language Model) for generating refined summaries
- Handling of both short documents and longer documents requiring chunk-based processing

### 3.4 Keyword Extractor (keyword_extractor.py)

The Keyword Extractor identifies and extracts relevant keywords from the document content. Main functionalities include:

- Preprocessing of text (tokenization, lemmatization, stopword removal)
- Extraction of keywords using TF-IDF and frequency analysis
- Dynamic adjustment of keyword count based on document length
- Refinement of keywords using the Groq LLM for improved contextual relevance

### 3.5 Database Manager (db_manager.py)

The Database Manager handles interactions with the MongoDB database for storing and retrieving processed document information. Key features include:

- Connection management with MongoDB
- CRUD operations (Create, Read, Update, Delete) for document records
- Schema creation and validation for the "documents" collection
- Error handling and logging for database operations

### 3.6 Performance Metrics (performance_metrics.py)

The Performance Metrics component monitors and records various performance-related data throughout the processing pipeline. Main functionalities include:

- Tracking of CPU and memory usage
- Measurement of processing time for individual documents and the entire batch
- Calculation of average performance metrics
- Saving of performance data to a file for later analysis

### 3.7 Utilities (utils.py)

The Utilities module provides common functions used across different components of the pipeline. Key utilities include:

- Extraction of paragraphs with boundaries from PDF text
- Merging of short paragraphs with overlap for improved context
- Classification of document length based on page count

## 4. Installation and Setup

To set up the Domain-Specific PDF Summarization & Keyword Extraction Pipeline, follow these steps:

1. Ensure you have Python 3.7+ installed on your system.
2. Clone the project repository from [repository URL].
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up a MongoDB instance (local or remote) and note the connection string.
5. Set the following environment variables:
   - `GROQ_API_KEY`: Your API key for the Groq LLM service
   - `MONGODB_CONNECTION_STRING`: The connection string for your MongoDB instance

## 5. Usage Instructions

To use the pipeline:

1. Place the PDF files you want to process in the designated input folder (default: `~/Desktop/pdf_folder`).
2. Run the main script:
   ```
   python main.py
   ```
3. The script will process all PDF files in the input folder, generating summaries and extracting keywords.
4. Processed document information will be stored in the MongoDB database.
5. Performance metrics will be saved to a file in the current directory.

## 6. Performance Considerations

The pipeline is designed with performance in mind, utilizing multi-threading for PDF processing. However, performance can be further optimized by:

- Adjusting the `max_workers` parameter in the `process_pdfs` function to match your system's capabilities.
- Fine-tuning the chunk size and overlap percentage in the `merge_short_paragraphs_with_overlap` function for optimal summarization performance.
- Monitoring and adjusting the MongoDB connection pool size based on your workload.

## 7. Error Handling and Logging

The pipeline implements comprehensive error handling and logging:

- Each component uses the Python `logging` module to record information, warnings, and errors.
- The main script sets up a rotating file handler to manage log files.
- Database operations include error handling to manage connection issues and invalid data.

Logs are stored in the `pdf_processor.log` file, which rotates when it reaches a size of 1MB, keeping up to 5 backup files.

## 8. Future Enhancements

Potential areas for future improvement include:

1. Implementation of a web-based user interface for easier interaction with the pipeline.
2. Integration with additional NLP models for improved summarization and keyword extraction.
3. Support for additional document formats beyond PDF.
4. Implementation of a queuing system for handling large batches of documents.
5. Addition of a document similarity feature to identify related documents in the corpus.

By leveraging this comprehensive Domain-Specific PDF Summarization & Keyword Extraction Pipeline, organizations can efficiently process large volumes of PDF documents, extract valuable insights, and make their document collections more searchable and analyzable.
