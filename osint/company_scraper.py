"""
Stage 1: OSINT Data Collection Engine
Company Scraper Module - Extracts data from company websites
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Set, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompanyScraper:
    """Scrapes publicly available company data from websites"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def scrape_company_data(self, company_name: str, website_url: str = None) -> Dict[str, List[str]]:
        """
        Scrape company-related data from website
        
        Args:
            company_name: Name of the target company
            website_url: Optional URL to scrape. If not provided, searches for company
            
        Returns:
            Dictionary containing keywords, products, executives, etc.
        """
        data = {
            'company_name': [company_name],
            'keywords': [],
            'products': [],
            'executives': [],
            'slogans': [],
            'locations': []
        }
        
        if not website_url:
            logger.warning(f"No URL provided for {company_name}. Using company name only.")
            data['keywords'].extend(self._extract_words(company_name))
            return data
        
        try:
            logger.info(f"Scraping {website_url}...")
            response = requests.get(website_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text from key pages
            data['keywords'].extend(self._extract_keywords(soup))
            data['products'].extend(self._extract_products(soup))
            data['executives'].extend(self._extract_executives(soup))
            data['slogans'].extend(self._extract_slogans(soup))
            data['locations'].extend(self._extract_locations(soup))
            
            # Try to find About Us page
            about_url = self._find_about_page(soup, website_url)
            if about_url:
                data = self._scrape_about_page(about_url, data)
                
        except requests.RequestException as e:
            logger.error(f"Error scraping {website_url}: {e}")
        
        # Clean and deduplicate
        for key in data:
            data[key] = list(set(filter(None, data[key])))
        
        return data
    
    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extract meaningful keywords from page"""
        keywords = []
        
        # Meta keywords
        meta_keywords = soup.find('meta', {'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords.extend(meta_keywords['content'].split(','))
        
        # Extract from headings
        for tag in ['h1', 'h2', 'h3']:
            for heading in soup.find_all(tag):
                text = heading.get_text().strip()
                keywords.extend(self._extract_words(text))
        
        return [kw.strip().lower() for kw in keywords if len(kw) > 2]
    
    def _extract_products(self, soup: BeautifulSoup) -> List[str]:
        """Extract product names"""
        products = []
        
        # Look for common product section patterns
        product_patterns = ['product', 'service', 'solution', 'offering']
        
        for pattern in product_patterns:
            sections = soup.find_all(class_=re.compile(pattern, re.I))
            for section in sections:
                text = section.get_text()
                products.extend(self._extract_capitalized_words(text))
        
        return products
    
    def _extract_executives(self, soup: BeautifulSoup) -> List[str]:
        """Extract executive names"""
        executives = []
        
        # Look for team/leadership sections
        team_sections = soup.find_all(class_=re.compile(r'(team|leadership|executive|founder)', re.I))
        
        for section in team_sections:
            text = section.get_text()
            # Simple name pattern: Capitalized words (2-3 words)
            names = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b', text)
            executives.extend(names)
        
        return executives
    
    def _extract_slogans(self, soup: BeautifulSoup) -> List[str]:
        """Extract slogans and taglines"""
        slogans = []
        
        # Check meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            slogans.append(meta_desc['content'])
        
        # Look for tagline classes
        taglines = soup.find_all(class_=re.compile(r'(tagline|slogan|motto)', re.I))
        for tag in taglines:
            slogans.append(tag.get_text().strip())
        
        return slogans
    
    def _extract_locations(self, soup: BeautifulSoup) -> List[str]:
        """Extract location/city names"""
        locations = []
        
        # Look for address sections
        address_sections = soup.find_all(['address', 'div'], class_=re.compile(r'(location|address|contact)', re.I))
        
        for section in address_sections:
            text = section.get_text()
            # Extract capitalized words that might be cities
            cities = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', text)
            locations.extend(cities)
        
        return locations
    
    def _find_about_page(self, soup: BeautifulSoup, base_url: str) -> str:
        """Find About Us page URL"""
        about_patterns = ['about', 'about-us', 'company', 'who-we-are']
        
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if any(pattern in href for pattern in about_patterns):
                return urljoin(base_url, link['href'])
        
        return None
    
    def _scrape_about_page(self, url: str, data: Dict) -> Dict:
        """Scrape About Us page for additional data"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all meaningful text
            text = soup.get_text()
            data['keywords'].extend(self._extract_words(text))
            
        except Exception as e:
            logger.error(f"Error scraping about page: {e}")
        
        return data
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract individual words from text"""
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        return [w.lower() for w in words]
    
    def _extract_capitalized_words(self, text: str) -> List[str]:
        """Extract capitalized words (likely proper nouns/product names)"""
        return re.findall(r'\b[A-Z][a-z]{2,}\b', text)


if __name__ == "__main__":
    # Test the scraper
    scraper = CompanyScraper()
    
    # Example usage
    test_data = scraper.scrape_company_data(
        company_name="Nexus Global",
        website_url="https://example.com"  # Replace with actual URL for testing
    )
    
    print("Scraped Data:")
    for key, values in test_data.items():
        print(f"{key}: {values[:5]}")  # Show first 5 items
