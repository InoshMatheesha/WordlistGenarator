"""
Social Engineering Wordlist Generator
Main CLI Application

Pure OSINT-based wordlist generator using social engineering techniques
No AI Required - Pattern-based mutations only

Generates 100 to 1,000,000 contextual passwords for security research
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

# Import our modules
from osint import OSINTEngine
from wordlist_engine import WordlistEngine
from config import OUTPUT_DIR, DEFAULT_MIN_PASSWORDS, DEFAULT_MAX_PASSWORDS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class WordlistGenerator:
    """Main application orchestrator"""
    
    def __init__(self):
        self.osint_engine = None
        self.ai_engine = None
        
    def run(self, args):
        """
        Execute the complete wordlist generation pipeline
        
        Args:
            args: Parsed command-line arguments
        """
        print("=" * 70)
        print("🔥 SOCIAL ENGINEERING WORDLIST GENERATOR 🔥")
        print("=" * 70)
        print()
        
        # Stage 1: OSINT Data Collection
        print("📍 STAGE 1: OSINT DATA COLLECTION ENGINE")
        print("-" * 70)
        
        self.osint_engine = OSINTEngine()
        
        # Collect company data
        if args.company:
            self.osint_engine.collect_company_data(
                company_name=args.company,
                website_url=args.website
            )
        
        # Collect username data
        if args.username:
            self.osint_engine.collect_username_data(args.username)
        
        # Load base wordlist
        if args.wordlist or args.words:
            self.osint_engine.load_base_wordlist(
                filepath=args.wordlist,
                words=args.words
            )
        
        # Get all collected keywords
        keywords = self.osint_engine.get_all_keywords()
        
        if not keywords:
            logger.error("❌ No data collected! Please provide at least one of:")
            logger.error("   --company, --username, --wordlist, or --words")
            sys.exit(1)
        
        print()
        print(f"✅ Stage 1 Complete!")
        print(f"   📊 Collected {len(keywords)} unique keywords")
        print(f"   📋 Sample: {', '.join(keywords[:10])}")
        print()
        
        # Stage 2: Wordlist Generation
        print("📍 STAGE 2: PATTERN-BASED MUTATION ENGINE")
        print("-" * 70)
        
        self.wordlist_engine = WordlistEngine()
        
        # Determine password count
        password_count = args.count
        
        # Validate count range
        if not (DEFAULT_MIN_PASSWORDS <= password_count <= DEFAULT_MAX_PASSWORDS):
            logger.warning(
                f"⚠️ Count adjusted to valid range: "
                f"{DEFAULT_MIN_PASSWORDS:,} - {DEFAULT_MAX_PASSWORDS:,}"
            )
            password_count = max(
                DEFAULT_MIN_PASSWORDS,
                min(password_count, DEFAULT_MAX_PASSWORDS)
            )
        
        # Generate passwords
        passwords = self.wordlist_engine.generate_passwords(
            keywords=keywords,
            target_count=password_count
        )
        
        print()
        print(f"✅ Stage 2 Complete!")
        print(f"   🎯 Generated {len(passwords):,} unique passwords")
        print()
        
        # Save output
        output_file = self._save_output(passwords, args)
        
        # Display summary
        self._display_summary(keywords, passwords, output_file)
        
        print()
        print("=" * 70)
        print("✨ GENERATION COMPLETE! ✨")
        print("=" * 70)
    
    def _save_output(self, passwords: list, args) -> Path:
        """
        Save generated passwords to file
        
        Args:
            passwords: List of generated passwords
            args: Command-line arguments
            
        Returns:
            Path to output file
        """
        # Determine output filename
        if args.output:
            # User specified a filename
            output_filename = args.output
            
            # Auto-add .txt extension if not present
            if not output_filename.endswith('.txt'):
                output_filename = f"{output_filename}.txt"
            
            # Save to output folder
            output_file = OUTPUT_DIR / output_filename
        else:
            # Auto-generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = OUTPUT_DIR / f"wordlist_{timestamp}.txt"
        
        # Ensure output directory exists
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            # Directory likely already exists, check if we can write to it
            if not output_file.parent.exists():
                logger.error(f"❌ Cannot create output directory: {e}")
                return None
        
        # Write passwords
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# Social Engineering Wordlist Generator\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total passwords: {len(passwords)}\n")
                f.write(f"# Method: OSINT + Pattern-based mutations\n")
                f.write(f"# For security research and penetration testing only\n")
                f.write(f"#\n")
                
                # Write passwords
                for password in passwords:
                    f.write(f"{password}\n")
            
            logger.info(f"💾 Saved {len(passwords):,} passwords to: {output_file}")
            
        except Exception as e:
            logger.error(f"❌ Error saving file: {e}")
            output_file = None
        
        return output_file
    
    def _display_summary(self, keywords: list, passwords: list, output_file: Path):
        """Display generation summary"""
        print()
        print("📊 GENERATION SUMMARY")
        print("-" * 70)
        print(f"   Input Keywords:     {len(keywords):,}")
        print(f"   Output Passwords:   {len(passwords):,}")
        
        if output_file:
            print(f"   Output File:        {output_file}")
            print(f"   File Size:          {output_file.stat().st_size / 1024:.2f} KB")
        
        print()
        print("   Sample Passwords (first 15):")
        for i, pwd in enumerate(passwords[:15], 1):
            print(f"      {i:2d}. {pwd}")
        
        if len(passwords) > 15:
            print(f"      ... and {len(passwords) - 15:,} more")


def parse_arguments():
    """Parse command-line arguments"""
    
    parser = argparse.ArgumentParser(
        description='🔥 Social Engineering Wordlist Generator (Pure OSINT)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Company-focused wordlist
  python main.py --company "Nexus Global" --website https://example.com --count 1000
  
  # Username-focused wordlist
  python main.py --username john_doe --count 500
  
  # Custom wordlist with base words
  python main.py --words "password,admin,login" --count 10000
  
  # Load from file and generate 100K passwords
  python main.py --wordlist base.txt --count 100000
  
  # Comprehensive scan (all options)
  python main.py --company "TechCorp" --website https://techcorp.com \\
                 --username admin --wordlist base.txt --count 50000

For security research and authorized penetration testing only!
        """
    )
    
    # OSINT Data Sources
    osint_group = parser.add_argument_group('🕸️  Stage 1: OSINT Data Sources')
    
    osint_group.add_argument(
        '-c', '--company',
        type=str,
        help='Target company name'
    )
    
    osint_group.add_argument(
        '-w', '--website',
        type=str,
        help='Company website URL to scrape'
    )
    
    osint_group.add_argument(
        '-u', '--username',
        type=str,
        help='Target username to search across platforms'
    )
    
    osint_group.add_argument(
        '-wl', '--wordlist',
        type=str,
        help='Path to base wordlist file (.txt)'
    )
    
    osint_group.add_argument(
        '-wd', '--words',
        type=str,
        help='Comma-separated words (e.g., "password,admin,login")'
    )
    
    # AI Generation Options
    generation_group = parser.add_argument_group('🔐 Generation Options')
    
    generation_group.add_argument(
        '-n', '--count',
        type=int,
        default=1000,
        help=f'Number of passwords to generate (min: {DEFAULT_MIN_PASSWORDS:,}, max: {DEFAULT_MAX_PASSWORDS:,})'
    )
    
    # Output Options
    output_group = parser.add_argument_group('💾 Output Options')
    
    output_group.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: output/wordlist_TIMESTAMP.txt)'
    )
    
    output_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (debug mode)'
    )
    
    args = parser.parse_args()
    
    # Validate that at least one input source is provided
    if not any([args.company, args.username, args.wordlist, args.words]):
        parser.error(
            "At least one data source is required:\n"
            "  --company, --username, --wordlist, or --words"
        )
    
    return args


def main():
    """Main entry point"""
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Create and run generator
        generator = WordlistGenerator()
        generator.run(args)
        
    except KeyboardInterrupt:
        print("\n\n❌ Generation cancelled by user")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
