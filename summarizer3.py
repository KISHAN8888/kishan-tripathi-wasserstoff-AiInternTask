import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
from utlis import extract_paragraphs_with_boundaries, merge_short_paragraphs_with_overlap
from PyPDF2 import PdfReader  # For getting the number of pages from the PDF

# Download necessary NLTK data
nltk.download('punkt')

class DynamicSummarizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def extract_key_sentences(self, paragraph, ratio=0.5):
        """
        Extract key sentences from the paragraph based on TF-IDF scores.
        Adjust the number of sentences based on paragraph length.
        """
        sentences = sent_tokenize(paragraph)
        num_sentences = len(sentences)
        
        if num_sentences == 0:
            return []  # Empty paragraph
        
        print(f"Processing paragraph with {num_sentences} sentences.")
        
        # Convert sentences to TF-IDF representation
        tfidf_matrix = self.vectorizer.fit_transform(sentences)
        sentence_scores = np.mean(tfidf_matrix.toarray(), axis=1)  # Score by averaging TF-IDF values

        # Determine how many sentences to select based on the length of the paragraph
        total_words = sum(len(word_tokenize(sent)) for sent in sentences)
        words_to_select = int(total_words * ratio)  # Select sentences covering about 1/3 of the paragraph's words
        
        selected_sentences = []
        selected_word_count = 0
        
        # Sort sentences by their TF-IDF scores in descending order
        sorted_indices = np.argsort(sentence_scores)[::-1]
        for idx in sorted_indices:
            selected_sentences.append(sentences[idx])
            selected_word_count += len(word_tokenize(sentences[idx]))
            if selected_word_count >= words_to_select:
                break
        
        print(f"Selected {len(selected_sentences)} sentences covering {selected_word_count} words (target was {words_to_select} words).")
        
        return selected_sentences

    def call_llm(self, sentences, is_final_summary=False):
        """
        Call the Groq LLM to generate a summary based on the key sentences.
        """
        if is_final_summary:
            prompt = (
                "You have now received summaries of various sections of a larger document. "
                "Based on these partial summaries, generate a final,summary that captures the overall "
                "main themes and key points of the document. Ensure the final summary flows smoothly "
                "and avoids any repetition.\n\n"
                f"{' '.join(sentences)}\n\n"
                "Generate the final, summary with size same exactly same as the input include evrything literally evrything properly just concatenate evrything well and strucutred so that it is descriptive based on the above content."
            )
        else:
            prompt = (
                "You are a helpful chatbot and an expert in extracting the main themes from a given document. "
                "You have been provided a set of documents below:\n\n"
                f"{' '.join(sentences)}\n\n"
                "Based on this set of documents, please identify the main themes. Avoid unnecessary introduction in the response."
            )
        print(f"Sending to Groq LLM: {prompt}")
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
            )
            summary = chat_completion.choices[0].message.content.strip()
            print(f"Generated summary: {summary}")
            return summary
        except Exception as e:
            print(f"Error calling Groq LLM: {e}")
            return ""
    
    def summarize_document(self, chunks,pdf_path):
        """
        Summarize the document. If the document has fewer than 3 pages, send the entire text
        to the LLM. Otherwise, process and summarize each paragraph.
        """
        # Get number of pages
        pdf_reader = PdfReader(pdf_path)
        num_pages = len(pdf_reader.pages)
#
        
        if num_pages < 3:
            # If the document has less than 3 pages, send the entire text to the LLM
            entire_text = " ".join(chunks)
            print(f"Document has {num_pages} pages. Sending the entire text to the LLM.")
            return self.call_llm([entire_text])
        else:
            # Otherwise, process the document in chunks and summarize each chunk
            all_summaries = []

            for i, chunk in enumerate(chunks):
                print(f"\nSummarizing chunk {i+1}/{len(chunks)}:")
                key_sentences = self.extract_key_sentences(chunk)
                if key_sentences:
                    summary = self.call_llm(key_sentences)
                    all_summaries.append(summary)
            
            
            final_concatenated_summary = " ".join(all_summaries)
            print("\nConcatenated summary of all chunks:\n", final_concatenated_summary)
            
            # Send the concatenated summary to the LLM for a refined final summary
            final_summary = self.call_llm([final_concatenated_summary], is_final_summary=True)
            print(final_summary)
            
            return final_summary

# Example usage:
if __name__ == "__main__":
    summarizer = DynamicSummarizer()

    pdf_path =  "C:\\Users\\kisha\\Desktop\\pdf_folder\\Operating System Notes.pdf"
    paragraphs = extract_paragraphs_with_boundaries(pdf_path)
    chunks = merge_short_paragraphs_with_overlap(paragraphs)
    
    summary = summarizer.summarize_document(chunks,pdf_path)
    print("\nFinal Summary:\n", summary)

