# PDF Summarization & Keyword Extraction Pipeline

## Overview

This project provides a powerful pipeline for processing PDF documents, generating summaries, and extracting keywords. It's designed for easy setup and use, making it ideal for researchers, data analysts, and anyone dealing with large volumes of PDF documents.

## Features

- 📄 Multi-threaded PDF processing
- 📝 Automatic text summarization
- 🔑 Intelligent keyword extraction
- 💾 MongoDB integration for data storage
- 📊 Performance monitoring

## Quick Start

### Prerequisites

- Python 3.7+
- MongoDB
- Groq API key (for LLM-based summarization)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pdf-summarization-pipeline.git
   cd pdf-summarization-pipeline
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following content:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   MONGODB_CONNECTION_STRING=your_mongodb_connection_string_here
   ```

### Usage

1. Place your PDF files in the `input_pdfs` folder.

2. Run the pipeline:
   ```
   python main.py
   ```

3. Find processed results in the MongoDB database and performance metrics in `performance_metrics_[timestamp].txt`.


## Troubleshooting

If you encounter any issues, please check the `pdf_processor.log` file for error messages. Common issues and their solutions are listed in the `TROUBLESHOOTING.md` file.

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines on how to submit issues, feature requests, and pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

- [PyPDF2](https://github.com/py-pdf/pypdf) for PDF processing
- [NLTK](https://www.nltk.org/) for natural language processing
- [Groq](https://groq.com/) for LLM-based summarization
- [MongoDB](https://www.mongodb.com/) for document storage

For a more detailed explanation of the project architecture and components, please refer to the `DOCUMENTATION.md` file.
