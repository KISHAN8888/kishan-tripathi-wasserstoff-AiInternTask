import pdfplumber

def extract_text_from_pdf(pdf_path, output_txt_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Initialize a variable to hold all extracted text
        full_text = ""
        
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract text from the current page
            page_text = page.extract_text()
            
            # Append the extracted text to full_text
            if page_text:
                full_text += page_text + "\n"  # Adding a newline between pages
        
    # Save the extracted text to a .txt file
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(full_text)

# Usage example:
pdf_path = "C:\\Users\\kisha\\Downloads\\Echo_report2.2.pdf"
output_txt_path = 'extracted_text.txt'
extract_text_from_pdf(pdf_path, output_txt_path)

print(f"Text extracted and saved to {output_txt_path}")
