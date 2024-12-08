import requests
from bs4 import BeautifulSoup
import nltk
from processing.classifier import Classifier
from processing.category_selector import CategorySelector
from preprocessing.news_extractor import NewsExtractor
from preprocessing.text_cleaner import TextCleaner

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_text_from_url(url):
    """Extract main text content from a URL using NewsExtractor"""
    try:
        extractor = NewsExtractor()
        html = extractor.fetch(url)
        content = extractor.extract_content(html)
        print("content: ")
        print(content)
        
        # Combine title and main content
        full_text = f"{content['title']} {content['text']}"
        print("full_text: ")
        print(full_text)
        # Clean the text
        cleaner = TextCleaner()
        cleaned_text = cleaner.preprocess(full_text)
        print("cleaned_text: ")
        print(cleaned_text)

        return cleaned_text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def categorize_url(url):
    """Categorize content from a URL"""
    # Initialize components
    classifier = Classifier()
    selector = CategorySelector()
    
    # Extract text from URL
    text = extract_text_from_url(url)
    if not text:
        return None
        
    # Perform classification
    classifications = classifier.classify(text)
    
    # Select best category
    result = selector.select(classifications)
    
    # Validate confidence
    if selector.validate_confidence(result["confidence"]):
        return result
    else:
        return {"category": "undefined", "confidence": 0.0}

def main():
    # url = "https://www.omgubuntu.co.uk/2024/12/linux-6-12-kernel-is-long-term-support"
    url = input("Enter the URL to categorize: ")
    result = categorize_url(url)
    
    if result:
        print(f"\nCategory: {result['category']}")
        print(f"Confidence: {result['confidence']:.2%}")
    else:
        print("Could not categorize the URL")

if __name__ == "__main__":
    main() 