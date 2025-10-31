"""
Social Engineering Wordlist Generator
Pure OSINT + Mutation Rules (No AI Required)
"""

import logging
from typing import List, Set
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordlistEngine:
    """
    Generate wordlists using social engineering techniques
    No AI - Pure pattern-based mutations
    """
    
    def __init__(self):
        self.mutations = []
    
    def generate_passwords(
        self,
        keywords: List[str],
        target_count: int = 1000
    ) -> List[str]:
        """
        Generate passwords from keywords using mutation rules
        
        Args:
            keywords: Base keywords from OSINT
            target_count: Number of passwords to generate
            
        Returns:
            List of generated passwords
        """
        logger.info(f"🔐 Starting wordlist generation...")
        logger.info(f"📊 Target: {target_count:,} passwords")
        logger.info(f"📋 Input keywords: {len(keywords)}")
        
        all_passwords = set()
        
        # 1. Add base keywords with common variations
        for word in keywords:
            all_passwords.add(word)
            all_passwords.add(word.lower())
            all_passwords.add(word.upper())
            all_passwords.add(word.capitalize())
            
            # Add common case variations
            all_passwords.add(word.title())  # Title Case
            if len(word) > 2:
                all_passwords.add(word[0].upper() + word[1:].lower())  # First letter caps
        
        logger.info(f"✓ Added {len(all_passwords)} base variations")
        
        # 2. Apply mutation rules
        all_passwords.update(self._apply_number_mutations(keywords))
        logger.info(f"✓ Applied number mutations: {len(all_passwords)} total")
        
        all_passwords.update(self._apply_special_char_mutations(keywords))
        logger.info(f"✓ Applied special char mutations: {len(all_passwords)} total")
        
        all_passwords.update(self._apply_leet_mutations(keywords))
        logger.info(f"✓ Applied leet speak mutations: {len(all_passwords)} total")
        
        all_passwords.update(self._apply_year_mutations(keywords))
        logger.info(f"✓ Applied year mutations: {len(all_passwords)} total")
        
        all_passwords.update(self._apply_combination_mutations(keywords))
        logger.info(f"✓ Applied word combinations: {len(all_passwords)} total")
        
        # 6. Apply advanced mutations (if we need more passwords)
        if len(all_passwords) < target_count:
            all_passwords.update(self._apply_advanced_mutations(keywords))
            logger.info(f"✓ Applied advanced mutations: {len(all_passwords)} total")
        
        # 7. Filter by length (6-20 characters)
        filtered = [pwd for pwd in all_passwords if 6 <= len(pwd) <= 20]
        
        # 4. Return requested count
        result = filtered[:target_count]
        
        logger.info(f"✅ Generation complete! Generated {len(result):,} passwords")
        
        return result
    
    def _apply_number_mutations(self, keywords: List[str]) -> Set[str]:
        """Add numbers to keywords - Common password patterns"""
        mutations = set()
        
        # Common number patterns (most popular first)
        common_numbers = [
            # Single digits
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            # Double digits (common ages, dates)
            '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31', '32', '33', '69', '88', '99', '00',
            # Triple digits
            '123', '321', '111', '222', '333', '420', '666', '777', '888', '999',
            # Common sequences
            '1234', '12345', '123456', '1234567', '12345678',
            '007', '101', '911',
            # Years (2-digit)
            '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
            '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
            # Years (4-digit)
            '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027'
        ]
        
        for word in keywords:
            for num in common_numbers:
                # Standard patterns: word + number
                mutations.add(f"{word}{num}")
                mutations.add(f"{word.capitalize()}{num}")
                mutations.add(f"{word.upper()}{num}")
                mutations.add(f"{word.lower()}{num}")
                
                # Number first patterns
                mutations.add(f"{num}{word}")
                mutations.add(f"{num}{word.capitalize()}")
        
        return mutations
    
    def _apply_special_char_mutations(self, keywords: List[str]) -> Set[str]:
        """Add special characters to keywords"""
        mutations = set()
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '_', '-', '.', '~', 
                        '!@', '!!', '!@#', '@#', '#$', '123!', '!123', '@123', 
                        '321', '111', '!@#$', '$$', '**', '__']
        
        for word in keywords:
            for char in special_chars:
                mutations.add(f"{word}{char}")
                mutations.add(f"{word.capitalize()}{char}")
                mutations.add(f"{word.upper()}{char}")
                mutations.add(f"{char}{word}")
        
        return mutations
    
    def _apply_leet_mutations(self, keywords: List[str]) -> Set[str]:
        """Apply leet speak transformations"""
        mutations = set()
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
            'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7'
        }
        
        for word in keywords:
            # Full leet
            leet_word = ''.join([leet_map.get(c, c) for c in word])
            if leet_word != word:
                mutations.add(leet_word)
                mutations.add(f"{leet_word}123")
                mutations.add(f"{leet_word}!")
            
            # Partial leet (only vowels)
            partial_leet = word
            for old, new in [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0')]:
                partial_leet = partial_leet.replace(old, new).replace(old.upper(), new)
            if partial_leet != word:
                mutations.add(partial_leet)
        
        return mutations
    
    def _apply_year_mutations(self, keywords: List[str]) -> Set[str]:
        """Add years to keywords"""
        mutations = set()
        years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027',
                 '20', '21', '22', '23', '24', '25', '26', '27',
                 '2019', '2018', '2017', '2016', '2015', '19', '18', '17', '16', '15']
        
        for word in keywords:
            for year in years:
                mutations.add(f"{word}{year}")
                mutations.add(f"{word.capitalize()}{year}")
                mutations.add(f"{word.upper()}{year}")
                mutations.add(f"{word}{year}!")
                mutations.add(f"{word.capitalize()}{year}@")
                mutations.add(f"{word}{year}#")
                mutations.add(f"{year}{word}")
        
        return mutations
    
    def _apply_combination_mutations(self, keywords: List[str]) -> Set[str]:
        """Combine multiple keywords"""
        mutations = set()
        
        # Combine pairs of keywords
        for i, word1 in enumerate(keywords[:10]):  # Limit to first 10 to avoid explosion
            for word2 in keywords[i+1:10]:
                mutations.add(f"{word1}{word2}")
                mutations.add(f"{word1.capitalize()}{word2}")
                mutations.add(f"{word1}{word2.capitalize()}")
                mutations.add(f"{word1}_{word2}")
                mutations.add(f"{word1}-{word2}")
                mutations.add(f"{word1}{word2}123")
        
        return mutations
    
    def _apply_advanced_mutations(self, keywords: List[str]) -> Set[str]:
        """Apply advanced mutation combinations to reach target count"""
        mutations = set()
        
        # More number variations
        for word in keywords:
            for i in range(1, 100):  # 1-99
                mutations.add(f"{word}{i}")
                if len(mutations) % 10 == 0:  # Also add capitalized versions every 10
                    mutations.add(f"{word.capitalize()}{i}")
            
            # Double numbers
            for num in ['11', '22', '33', '44', '55', '66', '77', '88', '99', '00']:
                mutations.add(f"{word}{num}")
                mutations.add(f"{word.upper()}{num}!")
            
            # Triple patterns
            for pattern in ['!!!', '@@@', '###', '...', '___']:
                mutations.add(f"{word}{pattern}")
            
            # More year combinations
            for year in range(2010, 2030):
                mutations.add(f"{word}{year}")
                mutations.add(f"{word}{str(year)[2:]}!")
            
            # Multi-char special combinations
            for combo in ['!@#', '@123', '#123', '$$$', '***', '!@#$', '1!', '2@', '3#']:
                mutations.add(f"{word}{combo}")
                mutations.add(f"{combo}{word}")
        
        return mutations


if __name__ == "__main__":
    # Test the engine
    print("🧪 Testing Wordlist Engine...")
    
    engine = WordlistEngine()
    
    test_keywords = ['admin', 'password', 'welcome', 'login', 'user']
    
    passwords = engine.generate_passwords(
        keywords=test_keywords,
        target_count=100
    )
    
    print(f"\n✅ Generated {len(passwords)} test passwords:")
    for i, pwd in enumerate(passwords[:20], 1):
        print(f"  {i}. {pwd}")
