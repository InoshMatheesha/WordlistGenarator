"""
Stage 1: OSINT Data Collection Engine
Username OSINT Module - Finds username across platforms
"""

import requests
import json
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UsernameScraper:
    """Find username across social media and online platforms"""
    
    def __init__(self):
        # Popular platforms to check (subset for educational purposes)
        self.platforms = {
            'GitHub': 'https://github.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'Instagram': 'https://instagram.com/{}',
            'Reddit': 'https://reddit.com/user/{}',
            'LinkedIn': 'https://linkedin.com/in/{}',
            'Facebook': 'https://facebook.com/{}',
            'YouTube': 'https://youtube.com/@{}',
            'TikTok': 'https://tiktok.com/@{}',
            'Medium': 'https://medium.com/@{}',
            'Dev.to': 'https://dev.to/{}',
            'GitLab': 'https://gitlab.com/{}',
            'Behance': 'https://behance.net/{}',
            'Dribbble': 'https://dribbble.com/{}',
            'Twitch': 'https://twitch.tv/{}',
            'Pinterest': 'https://pinterest.com/{}',
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def check_username(self, username: str) -> Dict[str, List[str]]:
        """
        Check if username exists on various platforms
        
        Args:
            username: Target username to search
            
        Returns:
            Dictionary with found platforms and extracted data
        """
        logger.info(f"Checking username: {username}")
        
        results = {
            'username': username,
            'found_platforms': [],
            'profile_urls': [],
            'variations': []
        }
        
        # Generate username variations
        results['variations'] = self._generate_variations(username)
        
        # Check platforms concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self._check_platform, platform, username): platform
                for platform in self.platforms
            }
            
            for future in as_completed(futures):
                platform = futures[future]
                try:
                    exists, url = future.result()
                    if exists:
                        results['found_platforms'].append(platform)
                        results['profile_urls'].append(url)
                        logger.info(f"✓ Found on {platform}")
                except Exception as e:
                    logger.debug(f"Error checking {platform}: {e}")
        
        return results
    
    def _check_platform(self, platform: str, username: str) -> tuple:
        """
        Check if username exists on a specific platform
        
        Returns:
            Tuple of (exists: bool, url: str)
        """
        url = self.platforms[platform].format(username)
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=5,
                allow_redirects=True
            )
            
            # Different platforms have different success indicators
            if response.status_code == 200:
                # Additional check: some platforms return 200 but show "not found"
                if 'not found' not in response.text.lower() and \
                   'doesn\'t exist' not in response.text.lower():
                    return (True, url)
            
            return (False, url)
            
        except requests.RequestException:
            return (False, url)
    
    def _generate_variations(self, username: str) -> List[str]:
        """
        Generate common username variations
        
        Args:
            username: Base username
            
        Returns:
            List of variations
        """
        variations = [username]
        
        # Common variations
        variations.append(username.lower())
        variations.append(username.upper())
        variations.append(username.capitalize())
        
        # With underscores
        if '_' not in username:
            variations.append(username + '_')
            variations.append('_' + username)
        
        # With numbers (common patterns)
        for num in ['1', '12', '123', '99', '00', '01']:
            variations.append(username + num)
            variations.append(num + username)
        
        # Leet speak common substitutions
        leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
        leet_version = username.lower()
        for char, replacement in leet_map.items():
            if char in leet_version:
                leet_version = leet_version.replace(char, replacement)
        variations.append(leet_version)
        
        # Remove duplicates
        return list(set(variations))
    
    def extract_keywords_from_username(self, username: str) -> List[str]:
        """
        Extract potential keywords from username
        
        Args:
            username: Username to analyze
            
        Returns:
            List of extracted keywords
        """
        import re
        
        keywords = []
        
        # Split by common separators
        parts = re.split(r'[_\-\.]', username)
        keywords.extend(parts)
        
        # Extract numbers
        numbers = re.findall(r'\d+', username)
        keywords.extend(numbers)
        
        # Extract alpha parts
        alpha_parts = re.findall(r'[a-zA-Z]+', username)
        keywords.extend(alpha_parts)
        
        return [k for k in keywords if len(k) > 1]


class SherlockWrapper:
    """
    Wrapper for Sherlock-like functionality
    Note: This is a simplified version. For production, use the actual Sherlock tool
    """
    
    @staticmethod
    def search(username: str) -> Dict:
        """
        Simplified sherlock-like search
        
        Args:
            username: Username to search
            
        Returns:
            Search results
        """
        scraper = UsernameScraper()
        return scraper.check_username(username)


if __name__ == "__main__":
    # Test the username scraper
    scraper = UsernameScraper()
    
    # Example usage
    test_username = "testuser123"
    results = scraper.check_username(test_username)
    
    print(f"\nUsername: {test_username}")
    print(f"Found on {len(results['found_platforms'])} platforms:")
    for platform in results['found_platforms']:
        print(f"  - {platform}")
    
    print(f"\nGenerated {len(results['variations'])} variations:")
    print(f"  {results['variations'][:10]}")  # Show first 10
