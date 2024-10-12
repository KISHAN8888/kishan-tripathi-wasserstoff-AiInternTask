import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
from test2parachunking import extract_paragraphs_with_boundaries
from test2parachunking import merge_short_paragraphs

# Download necessary NLTK data
nltk.download('punkt')

class DynamicSummarizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
        prompt = "Summarize the following text in about 30 words and give only summary text nothing like this:Here is a summary of the text in about 30 words: :\n" + " ".join(sentences)
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
    
    def summarize_document(self, chunks):
        """
        Summarize the entire document by processing each chunk (provided as a list of strings),
        extracting key sentences, and summarizing each chunk using the LLM.
        """
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

    pdf_path = "C:\\Users\\kisha\\Downloads\\Echo_report2.2.pdf"
    paragraphs = extract_paragraphs_with_boundaries(pdf_path)

# Merge paragraphs that have fewer than 50 words
    chunks = merge_short_paragraphs(paragraphs)  
    
    # Example: List of string chunks (instead of a single text string)
    #chunks = [
    #    "At EY, our purpose is to build a better working world. We help digital pioneers fight data piracy, guide governments through crises, and unlock new treatments with data analytics.",
    #    "Our Consulting practice provides technology consulting services, using disruptive technology like AI, blockchain, and cloud. We aim to solve complex business problems.",
    #    "Cybersecurity has become a top priority for businesses. We help clients quantify risks and embed security in digital initiatives from day one."
    #]

    summary = summarizer.summarize_document(chunks)
    print("\nFinal Summary:\n", summary)
