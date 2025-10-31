"""
Stage 1: OSINT Data Collection Engine
Main orchestrator for all data collection modules
"""

from typing import Dict, List
import logging
from .company_scraper import CompanyScraper
from .username_scraper import UsernameScraper
from .wordlist_processor import WordlistProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OSINTEngine:
    """Main engine for OSINT data collection"""
    
    def __init__(self):
        self.company_scraper = CompanyScraper()
        self.username_scraper = UsernameScraper()
        self.wordlist_processor = WordlistProcessor()
        self.collected_data = {
            'keywords': [],
            'variations': [],
            'context': {}
        }
    
    def collect_company_data(self, company_name: str, website_url: str = None) -> Dict:
        """
        Collect company-related data
        
        Args:
            company_name: Name of the company
            website_url: Optional company website URL
            
        Returns:
            Collected company data
        """
        logger.info(f"🕸️ Collecting company data for: {company_name}")
        
        data = self.company_scraper.scrape_company_data(company_name, website_url)
        
        # Flatten all data into keywords
        all_keywords = []
        for key, values in data.items():
            all_keywords.extend(values)
        
        self.collected_data['keywords'].extend(all_keywords)
        self.collected_data['context']['company'] = data
        
        logger.info(f"✓ Collected {len(all_keywords)} company-related keywords")
        return data
    
    def collect_username_data(self, username: str) -> Dict:
        """
        Collect username-related data
        
        Args:
            username: Target username
            
        Returns:
            Username search results
        """
        logger.info(f"🕸️ Collecting username data for: {username}")
        
        data = self.username_scraper.check_username(username)
        
        # Add username and variations to keywords
        self.collected_data['keywords'].append(username)
        self.collected_data['variations'].extend(data['variations'])
        self.collected_data['context']['username'] = data
        
        logger.info(f"✓ Found username on {len(data['found_platforms'])} platforms")
        logger.info(f"✓ Generated {len(data['variations'])} variations")
        
        return data
    
    def load_base_wordlist(self, filepath: str = None, words: str = None):
        """
        Load base wordlist from file or string
        
        Args:
            filepath: Path to wordlist file
            words: Comma-separated words string
        """
        logger.info("🕸️ Loading base wordlist...")
        
        if filepath:
            loaded_words = self.wordlist_processor.load_from_file(filepath)
            self.collected_data['keywords'].extend(loaded_words)
        
        if words:
            self.wordlist_processor.add_manual_words(words)
            self.collected_data['keywords'].extend(words.split(','))
        
        logger.info(f"✓ Base wordlist loaded")
    
    def get_all_keywords(self) -> List[str]:
        """
        Get all collected keywords (deduplicated)
        
        Returns:
            List of unique keywords
        """
        # Combine keywords and variations
        all_words = self.collected_data['keywords'] + self.collected_data['variations']
        
        # Clean and deduplicate
        cleaned = []
        for word in all_words:
            if isinstance(word, str):
                word = word.strip()
                if word and len(word) > 2:
                    cleaned.append(word)
        
        return list(set(cleaned))
    
    def get_summary(self) -> Dict:
        """
        Get summary of collected data
        
        Returns:
            Summary dictionary
        """
        keywords = self.get_all_keywords()
        
        summary = {
            'total_keywords': len(keywords),
            'sample_keywords': keywords[:20],
            'company_data': self.collected_data['context'].get('company', {}),
            'username_data': self.collected_data['context'].get('username', {}),
        }
        
        return summary
    
    def prepare_for_ai(self) -> str:
        """
        Prepare collected data as a formatted string for AI processing
        
        Returns:
            Formatted string with all collected data
        """
        context = self.collected_data['context']
        
        output = "=== OSINT DATA COLLECTION ===\n\n"
        
        # Company data
        if 'company' in context:
            company = context['company']
            output += f"COMPANY: {company.get('company_name', ['Unknown'])[0]}\n"
            
            if company.get('products'):
                output += f"PRODUCTS: {', '.join(company['products'][:10])}\n"
            
            if company.get('keywords'):
                output += f"KEYWORDS: {', '.join(company['keywords'][:20])}\n"
            
            if company.get('executives'):
                output += f"EXECUTIVES: {', '.join(company['executives'][:5])}\n"
            
            output += "\n"
        
        # Username data
        if 'username' in context:
            username = context['username']
            output += f"USERNAME: {username.get('username', 'Unknown')}\n"
            
            if username.get('found_platforms'):
                output += f"FOUND ON: {', '.join(username['found_platforms'])}\n"
            
            output += "\n"
        
        # All keywords
        all_keywords = self.get_all_keywords()
        output += f"TOTAL UNIQUE KEYWORDS: {len(all_keywords)}\n"
        output += f"SAMPLE KEYWORDS: {', '.join(all_keywords[:30])}\n"
        
        return output


if __name__ == "__main__":
    # Test the OSINT engine
    engine = OSINTEngine()
    
    # Example: Collect company data
    engine.collect_company_data("Nexus Global")
    
    # Example: Collect username data
    engine.collect_username_data("john_doe")
    
    # Example: Load base wordlist
    engine.load_base_wordlist(words="password,admin,login,welcome")
    
    # Get summary
    summary = engine.get_summary()
    print(f"\n📊 OSINT Summary:")
    print(f"Total keywords collected: {summary['total_keywords']}")
    print(f"Sample: {summary['sample_keywords'][:10]}")
    
    # Prepare for AI
    ai_input = engine.prepare_for_ai()
    print(f"\n🤖 Prepared for AI processing:")
    print(ai_input[:500] + "...")
