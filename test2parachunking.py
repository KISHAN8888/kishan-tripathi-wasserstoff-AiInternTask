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

    return paragraph_info

def merge_short_paragraphs(paragraphs, word_threshold=50):
    merged_paragraphs = []
    temp_paragraph = ""
    
    for i, para_info in enumerate(paragraphs):
        paragraph = para_info['paragraph_text']
        word_count = len(paragraph.split())

        if word_count < word_threshold:
            # Merge with the next paragraph if current paragraph has fewer than 50 words
            if temp_paragraph:
                temp_paragraph += " " + paragraph
            else:
                temp_paragraph = paragraph
        else:
            # If the paragraph is larger than 50 words or temp_paragraph already contains some text
            if temp_paragraph:
                merged_paragraphs.append(temp_paragraph + " " + paragraph)
                temp_paragraph = ""  # Reset the temp paragraph
            else:
                merged_paragraphs.append(paragraph)

    # If the last temp_paragraph was too short and didn't get appended
    if temp_paragraph:
        merged_paragraphs.append(temp_paragraph)

    return merged_paragraphs

## Use the function on your PDF
pdf_path = "C:\\Users\\kisha\\Documents\\Sem 5\\a-beginners-guide-to-data-and-analytics.pdf"
paragraphs = extract_paragraphs_with_boundaries(pdf_path)

# Merge paragraphs that have fewer than 50 words
final_paragraphs = merge_short_paragraphs(paragraphs)

# Output the total number of final paragraphs (chunks)
print(f"Total Number of Final Paragraphs (Chunks): {len(final_paragraphs)}")

# Output each final paragraph
for index, paragraph in enumerate(final_paragraphs):
    print(f"Paragraph {index + 1}:")
    print(paragraph)
    print("-" * 50)

print(final_paragraphs)    
