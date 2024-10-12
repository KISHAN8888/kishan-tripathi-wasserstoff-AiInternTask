import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import string

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class KeywordExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        # Remove punctuation and numbers
        tokens = [token for token in tokens if token.isalpha()]
        # Remove stop words and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return tokens

    def extract_tfidf_keywords(self, text, num_keywords):
        # Create TfidfVectorizer object
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # Fit and transform the text
        tfidf_matrix = tfidf_vectorizer.fit_transform([text])
        # Get feature names (words)
        feature_names = tfidf_vectorizer.get_feature_names_out()
        # Get TF-IDF scores
        tfidf_scores = tfidf_matrix.toarray()[0]
        # Create a dictionary of words and their TF-IDF scores
        word_scores = {word: score for word, score in zip(feature_names, tfidf_scores)}
        # Sort words by TF-IDF score in descending order and get top keywords
        sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        return [word for word, score in sorted_words[:num_keywords]]

    def extract_frequency_keywords(self, text, num_keywords):
        tokens = self.preprocess_text(text)
        # Count word frequencies
        word_freq = Counter(tokens)
        # Get top keywords based on frequency
        return [word for word, _ in word_freq.most_common(num_keywords)]

    def extract_keywords(self, text, num_keywords=10):
        tfidf_keywords = set(self.extract_tfidf_keywords(text, num_keywords))
        freq_keywords = set(self.extract_frequency_keywords(text, num_keywords))
        # Combine and prioritize keywords
        combined_keywords = list(tfidf_keywords.union(freq_keywords))
        return combined_keywords[:num_keywords]



# Usage example
if __name__ == "__main__":
    extractor = KeywordExtractor()
    
    # Example text (you would replace this with actual document content)
    text = """
    UNIT 2  

 
    """
    
    keywords = extractor.extract_keywords(text, num_keywords=20)
    print("Extracted Keywords:")
    print(keywords)
