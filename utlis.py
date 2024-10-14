from PyPDF2 import PdfReader
import re

def extract_paragraphs_with_boundaries(pdf_path, max_words=1500):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    raw_paragraphs = re.split(r'\n\s*\n', text.strip())
    paragraph_info = []
    current_position = 0
    current_paragraph = ""
    
    for raw_paragraph in raw_paragraphs:
        words = raw_paragraph.split()
        for word in words:
            if len(current_paragraph.split()) < max_words:
                if current_paragraph:
                    current_paragraph += " " + word
                else:
                    current_paragraph = word
            else:
                paragraph_start = current_position
                paragraph_end = current_position + len(current_paragraph)
                paragraph_info.append({
                    'paragraph_index': len(paragraph_info) + 1,
                    'paragraph_start': paragraph_start,
                    'paragraph_end': paragraph_end,
                    'paragraph_text': current_paragraph
                })
                current_position = paragraph_end + 1
                current_paragraph = word
        
        
        if current_paragraph:
            paragraph_start = current_position
            paragraph_end = current_position + len(current_paragraph)
            paragraph_info.append({
                'paragraph_index': len(paragraph_info) + 1,
                'paragraph_start': paragraph_start,
                'paragraph_end': paragraph_end,
                'paragraph_text': current_paragraph
            })
            current_position = paragraph_end + 2
            current_paragraph = ""
    
    return paragraph_info

def merge_short_paragraphs_with_overlap(paragraphs, word_threshold=500, max_words=4000, overlap_percentage=0.1):
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
                merged_paragraph = temp_paragraph + " " + paragraph
            else:
                merged_paragraph = paragraph
            
            # Split if the merged paragraph exceeds max_words
            while len(merged_paragraph.split()) > max_words:
                split_point = max_words
                while split_point > 0 and merged_paragraph[split_point] != ' ':
                    split_point -= 1
                
                if merged_paragraphs:
                    prev_paragraph = merged_paragraphs[-1]
                    overlap_words = int(len(prev_paragraph.split()) * overlap_percentage)
                    current_chunk = " ".join(prev_paragraph.split()[-overlap_words:]) + " " + merged_paragraph[:split_point]
                else:
                    current_chunk = merged_paragraph[:split_point]
                
                merged_paragraphs.append(current_chunk)
                merged_paragraph = merged_paragraph[split_point:].strip()
            
            if merged_paragraph:
                if merged_paragraphs:
                    prev_paragraph = merged_paragraphs[-1]
                    overlap_words = int(len(prev_paragraph.split()) * overlap_percentage)
                    merged_paragraph = " ".join(prev_paragraph.split()[-overlap_words:]) + " " + merged_paragraph
                merged_paragraphs.append(merged_paragraph)
            
            temp_paragraph = ""
    
    if temp_paragraph:
        if merged_paragraphs:
            prev_paragraph = merged_paragraphs[-1]
            overlap_words = int(len(prev_paragraph.split()) * overlap_percentage)
            temp_paragraph = " ".join(prev_paragraph.split()[-overlap_words:]) + " " + temp_paragraph
        merged_paragraphs.append(temp_paragraph)
    
    return merged_paragraphs

def classify_document_length(num_pages):
    try:
        num_pages = int(num_pages)
        if num_pages <= 5:
            return "short"
        elif num_pages <= 30:
            return "medium"
        else:
            return "long"
    except ValueError:
        return "unknown"


# pdf_path = "path/to/your/pdf/file.pdf"
# paragraphs = extract_paragraphs_with_boundaries(pdf_path, max_words=1500)
# final_paragraphs = merge_and_split_paragraphs(paragraphs, word_threshold=500, max_words=1500, overlap_percentage=0.1)
# 
# print(f"Total Number of Final Paragraphs (Chunks): {len(final_paragraphs)}")
# 
# for index, paragraph in enumerate(final_paragraphs):
#     print(f"Paragraph {index + 1}:")
#     print(paragraph)
#     print("-" * 50)


#pdf_path = "C:\\Users\\kisha\\Desktop\\pdf_folder\\yolov1-yolov10.pdf"
#paragraphs = extract_paragraphs_with_boundaries(pdf_path)
#final_paragraphs = merge_short_paragraphs_with_overlap(paragraphs, word_threshold=500, max_words=1500, overlap_percentage=0.1)
#
#
#
#for index, paragraph in enumerate(final_paragraphs):
#    print(f"Paragraph {index + 1}:")
#    print(paragraph)
#    print("-" * 50)
#    
#print(f"Total Number of Final Paragraphs (Chunks): {len(final_paragraphs)}")    