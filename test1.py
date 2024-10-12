from PyPDF2 import PdfReader
import re

def extract_paragraphs_with_boundaries(pdf_path):
    # Open the PDF and extract text
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Split the text into paragraphs using double newlines or your custom delimiter
    paragraphs = re.split(r'\n\s*\n', text.strip())

    # Store paragraph start and end info
    paragraph_info = []
    current_position = 0  # Track the current position in the text

    for para_index, paragraph in enumerate(paragraphs):
        paragraph_start = current_position  # Mark the starting character of the paragraph
        paragraph_end = paragraph_start + len(paragraph)  # Mark the ending character of the paragraph
        current_position = paragraph_end + 2  # Update position (+2 for newlines)
        
        paragraph_info.append({
            'paragraph_index': para_index + 1,
            'paragraph_start': paragraph_start,
            'paragraph_end': paragraph_end,
            'paragraph_text': paragraph
        })

    return paragraph_info, len(paragraphs)  # Return the paragraphs and the total count

def get_paragraph_chunks(paragraphs):
    # Treat each paragraph as a chunk
    chunks = [para_info['paragraph_text'] for para_info in paragraphs]
    return chunks

# Use the function on your PDF
pdf_path = "C:\\Users\\kisha\\Downloads\\Consulting - Engg JD 2024.pdf"
paragraphs, total_paragraphs = extract_paragraphs_with_boundaries(pdf_path)

# Output the total number of paragraphs (equal to chunks)
print(f"Total Number of Paragraphs (Chunks): {total_paragraphs}")

# Output each chunk (paragraph) as its own unit
for para_info in paragraphs:
    print(f"Paragraph {para_info['paragraph_index']}:")
    print(f"Start: {para_info['paragraph_start']}, End: {para_info['paragraph_end']}")
    print(f"Chunk (Full Paragraph): {para_info['paragraph_text']}")
    print("-" * 50)


print(paragraphs)
print(total_paragraphs)

print(f"Total Number of Paragraphs (Chunks): {total_paragraphs}")
