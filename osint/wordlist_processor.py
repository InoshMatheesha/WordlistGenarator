"""
Stage 1: OSINT Data Collection Engine
Wordlist Processor - Handles base wordlist files
"""

import logging
from pathlib import Path
from typing import List, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordlistProcessor:
    """Process and manage base wordlists"""
    
    def __init__(self):
        self.wordlist = set()
    
    def load_from_file(self, filepath: str) -> List[str]:
        """
        Load words from a text file
        
        Args:
            filepath: Path to the wordlist file
            
        Returns:
            List of words
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return []
        
        logger.info(f"Loading wordlist from {filepath}...")
        
        words = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip()
                    if word and not word.startswith('#'):  # Skip comments
                        words.append(word)
            
            logger.info(f"Loaded {len(words)} words from file")
            self.wordlist.update(words)
            
        except Exception as e:
            logger.error(f"Error loading file: {e}")
        
        return words
    
    def add_words(self, words: List[str]):
        """
        Add words to the wordlist
        
        Args:
            words: List of words to add
        """
        self.wordlist.update(words)
        logger.info(f"Added {len(words)} words to wordlist")
    
    def add_manual_words(self, words_string: str):
        """
        Add words from a comma-separated string
        
        Args:
            words_string: Comma-separated words
        """
        words = [w.strip() for w in words_string.split(',')]
        self.add_words(words)
    
    def get_wordlist(self) -> List[str]:
        """
        Get the current wordlist
        
        Returns:
            List of unique words
        """
        return list(self.wordlist)
    
    def filter_by_length(self, min_length: int = 3, max_length: int = 50) -> List[str]:
        """
        Filter words by length
        
        Args:
            min_length: Minimum word length
            max_length: Maximum word length
            
        Returns:
            Filtered word list
        """
        return [w for w in self.wordlist if min_length <= len(w) <= max_length]
    
    def save_to_file(self, filepath: str, words: List[str] = None):
        """
        Save wordlist to file
        
        Args:
            filepath: Output file path
            words: Words to save (if None, uses internal wordlist)
        """
        if words is None:
            words = self.get_wordlist()
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for word in sorted(set(words)):
                    f.write(f"{word}\n")
            
            logger.info(f"Saved {len(words)} words to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
    
    def extract_from_text(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract words from arbitrary text
        
        Args:
            text: Input text
            min_length: Minimum word length
            
        Returns:
            List of extracted words
        """
        import re
        
        # Extract alphanumeric words
        words = re.findall(r'\b\w+\b', text)
        
        # Filter and clean
        words = [w for w in words if len(w) >= min_length]
        
        return words
    
    def get_statistics(self) -> dict:
        """
        Get wordlist statistics
        
        Returns:
            Dictionary with statistics
        """
        words = list(self.wordlist)
        
        if not words:
            return {
                'total_words': 0,
                'avg_length': 0,
                'min_length': 0,
                'max_length': 0
            }
        
        lengths = [len(w) for w in words]
        
        return {
            'total_words': len(words),
            'avg_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'unique_words': len(set(words))
        }


if __name__ == "__main__":
    # Test the wordlist processor
    processor = WordlistProcessor()
    
    # Add some test words
    processor.add_manual_words("password, admin, user, login, welcome")
    
    # Get statistics
    stats = processor.get_statistics()
    print(f"Wordlist Statistics: {stats}")
    
    # Filter by length
    filtered = processor.filter_by_length(min_length=4)
    print(f"Filtered words (min 4 chars): {filtered}")
