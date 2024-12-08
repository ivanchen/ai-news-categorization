from bs4 import BeautifulSoup
import requests

# HOW TO USE IT
# extractor = NewsExtractor()
# try:
#     html = extractor.fetch("https://example.com/news-article")
#     content = extractor.extract_content(html)
#     print(f"Title: {content['title']}")
#     print(f"Date: {content['date']}")
#     print(f"Content: {content['text'][:200]}...")  # First 200 chars
# except Exception as e:
#     print(f"Error: {e}")

class NewsExtractor:
    def fetch(self, url):
        """Fetch and parse HTML content from a URL
        
        Args:
            url (str): The URL of the news article
            
        Returns:
            str: Raw HTML content
            
        Raises:
            RequestException: If the URL cannot be accessed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch content from {url}: {str(e)}")

    def extract_content(self, html):
        """Extract relevant content from HTML
        
        Args:
            html (str): Raw HTML content
            
        Returns:
            dict: Extracted content with keys 'title', 'text', 'date' (if available)
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title (usually in h1 or article title)
            title = ''
            title_tag = soup.find('h1') or soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
            
            # Extract main content (looking for common article containers)
            content = ''
            article_tags = soup.find('article') or soup.find('main') or soup.find(class_=['article-content', 'content', 'story-body'])
            
            if article_tags:
                # Get all paragraphs
                paragraphs = article_tags.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
            else:
                # Fallback: get all paragraphs from body
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
            
            # Try to extract date (this is more complex as date formats vary)
            date = ''
            date_tags = soup.find(class_=['date', 'article-date', 'publish-date'])
            if date_tags:
                date = date_tags.get_text().strip()
            
            return {
                'title': title,
                'text': content,
                'date': date
            }
            
        except Exception as e:
            raise Exception(f"Failed to extract content: {str(e)}")
