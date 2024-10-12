import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq

# Download necessary NLTK data
nltk.download('punkt')

class DynamicSummarizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def preprocess(self, text):
        """
        Preprocess the text by tokenizing into paragraphs.
        """
        paragraphs = text.split('\n\n')  # Simple split by double newlines
        paragraphs = [p.strip() for p in paragraphs if p.strip()]  # Remove empty paragraphs
        return paragraphs

    def get_paragraph_chunks(self, text):
        """
        Split the job description into paragraphs and merge small chunks.
        """
        # Split the text into paragraphs
        paragraphs = [para.strip() for para in text.strip().split('\n\n') if para.strip()]
        
        # Final list of chunks
        final_chunks = []
        temp_chunk = ""
        
        for para in paragraphs:
            # If the temp_chunk is not empty, add it to the final_chunks
            if temp_chunk:
                temp_chunk += " " + para
            else:
                temp_chunk = para
            
            # If the current word count plus temp_chunk's count is less than 50, continue merging
            if len(temp_chunk.split()) < 50:
                continue
            else:
                final_chunks.append(temp_chunk)
                temp_chunk = ""
        
        # Add any remaining chunk if it's not empty
        if temp_chunk:
            final_chunks.append(temp_chunk)
        
        return final_chunks

    def extract_key_sentences(self, paragraph, ratio=0.33):
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

    def call_llm(self, sentences):
        """
        Call the Groq LLM to generate a summary based on the key sentences.
        """
        prompt = "Summarize the following text in about 20 words:\n" + " ".join(sentences)
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
    
    def summarize_document(self, text):
        """
        Summarize the entire document by dividing it into paragraphs, extracting key sentences,
        and summarizing each paragraph using the LLM.
        """
        chunks = self.get_paragraph_chunks(text)  # Get the chunks instead of paragraphs
        all_summaries = []

        for i, chunk in enumerate(chunks):
            print(f"\nSummarizing chunk {i+1}/{len(chunks)}:")
            key_sentences = self.extract_key_sentences(chunk)
            if key_sentences:
                summary = self.call_llm(key_sentences)
                all_summaries.append(summary)
        
        final_summary = " ".join(all_summaries)
        return final_summary

# Example usage:
if __name__ == "__main__":
    summarizer = DynamicSummarizer()
    
    text = """
                                                                                                                                               
    """

    summary = summarizer.summarize_document(text)
    print("\nFinal Summary:\n", summary)
