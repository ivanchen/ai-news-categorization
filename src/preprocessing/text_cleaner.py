import re
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

## To use this class:
# cleaner = TextCleaner()
# text = "Here's some sample text with HTML <p>tags</p> and numbers 123!"
# processed_text = cleaner.preprocess(text)
# print(processed_text)
## Output: "sample text tag"

class TextCleaner:
    def __init__(self):
        # Download required NLTK data only if not already present
        for resource in ['punkt', 'stopwords', 'wordnet']:
            try:
                nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' 
                              else f'corpora/{resource}')
            except LookupError:
                nltk.download(resource)
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean(self, text):
        """Text cleaning operations"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def normalize(self, text):
        """Text normalization"""
        # Force download punkt if not present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Tokenization - using a simpler split first to debug
        tokens = text.split()  # Fallback simple tokenization
        
        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatization
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # Join tokens back into text
        normalized_text = ' '.join(tokens)
        
        return normalized_text

    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        # Clean the text
        cleaned_text = self.clean(text)
        
        # Normalize the text
        normalized_text = self.normalize(cleaned_text)
        
        return normalized_text
