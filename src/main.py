import requests
from bs4 import BeautifulSoup
import nltk
from processing.classifier import Classifier
from processing.category_selector import CategorySelector
from preprocessing.news_extractor import NewsExtractor
from preprocessing.text_cleaner import TextCleaner
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def fetch_with_selenium(url):
    """Fetch content using Selenium for JavaScript-heavy sites"""
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        # Wait for content to load
        time.sleep(3)  # Simple wait, or use WebDriverWait for specific elements
        return driver.page_source
    finally:
        driver.quit()

def extract_text_from_url(url):
    """Extract main text content from a URL using NewsExtractor"""
    try:
        extractor = NewsExtractor()
        
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        # Add retry mechanism with delay
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                html = response.text
                if html:
                    break
                time.sleep(retry_delay)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(retry_delay)
        
        # Verify we have content
        if not html or len(html.strip()) < 100:  # Arbitrary minimum length
            raise ValueError("Retrieved content appears to be empty or too short")
            
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