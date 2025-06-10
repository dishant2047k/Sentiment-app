import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import re

class ReviewScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
        }
        
    def get_page(self, url):
        """Fetch a webpage with random user agent and delays"""
        self.headers['User-Agent'] = self.ua.random
        try:
            # Random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_amazon_reviews(self, url):
        """Scrape reviews from Amazon product page"""
        html = self.get_page(url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        reviews = []
        
        # Find review containers - Amazon has multiple possible structures
        review_containers = soup.find_all('div', {'data-hook': 'review'})
        if not review_containers:
            review_containers = soup.find_all('div', class_='a-section review')
        
        for review in review_containers:
            text = ''
            # Try different selectors for review text
            text_element = review.find('span', {'data-hook': 'review-body'})
            if not text_element:
                text_element = review.find('div', class_='review-text')
            
            if text_element:
                text = text_element.get_text(strip=True)
                # Clean up the text
                text = re.sub(r'\s+', ' ', text).strip()
                if text and text.lower() not in ['the media could not be loaded.', '']:
                    reviews.append(text)
        
        return reviews
    
    def scrape_generic_reviews(self, url, review_class=None):
        """Scrape reviews from generic websites"""
        html = self.get_page(url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        reviews = []
        
        # Try to find common review containers
        selectors = [
            {'class': 'review'},
            {'class': 'review-text'},
            {'class': 'customer-review'},
            {'itemprop': 'reviewBody'},
            {'data-test': 'review-description'},
        ]
        
        if review_class:
            selectors.insert(0, {'class': review_class})
            
        for selector in selectors:
            review_elements = soup.find_all('div', selector)
            if review_elements:
                for element in review_elements:
                    text = element.get_text(strip=True)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text:
                        reviews.append(text)
                break
        
        return reviews
    
    def scrape_reviews(self, url, site_type='auto'):
        """
        Main scraping function
        :param url: URL of the product page with reviews
        :param site_type: 'amazon', 'generic', or 'auto' for automatic detection
        :return: List of review texts
        """
        if site_type == 'auto':
            if 'amazon.' in url.lower():
                site_type = 'amazon'
            else:
                site_type = 'generic'
        
        if site_type == 'amazon':
            return self.scrape_amazon_reviews(url)
        else:
            return self.scrape_generic_reviews(url)

# Example usage
if __name__ == "__main__":
    scraper = ReviewScraper()
    
    # Amazon example
    amazon_url = "https://www.amazon.com/product-reviews/B08N5KWB9H/"
    print("Scraping Amazon reviews...")
    amazon_reviews = scraper.scrape_reviews(amazon_url)
    print(f"Found {len(amazon_reviews)} Amazon reviews")
    
    # Generic site example (you'll need to provide a real URL)
    generic_url = "https://www.example.com/product/reviews"
    print("\nScraping generic site reviews...")
    generic_reviews = scraper.scrape_reviews(generic_url)
    print(f"Found {len(generic_reviews)} generic reviews")
    
    # Print sample reviews
    if amazon_reviews:
        print("\nSample Amazon reviews:")
        for i, review in enumerate(amazon_reviews[:3], 1):
            print(f"{i}. {review[:200]}...")
    
    if generic_reviews:
        print("\nSample generic reviews:")
        for i, review in enumerate(generic_reviews[:3], 1):
            print(f"{i}. {review[:200]}...")