"""
Configuration file for Social Engineering Wordlist Generator
Pure OSINT - No AI Required
"""

from pathlib import Path
import os

# Output Configuration
OUTPUT_DIR = Path('output')

# Create output directory if it doesn't exist (handle permission errors gracefully)
try:
    OUTPUT_DIR.mkdir(exist_ok=True)
except (PermissionError, OSError):
    # Directory might already exist or have permission issues
    # Check if it exists and is accessible
    if not OUTPUT_DIR.exists():
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
        except:
            # Fallback: use current directory if output/ can't be created
            print(f"Warning: Could not create output directory. Using current directory.")
            OUTPUT_DIR = Path('.')

# Generation Settings
DEFAULT_MIN_PASSWORDS = 100
DEFAULT_MAX_PASSWORDS = 1000000

# OSINT Settings
REQUEST_TIMEOUT = 10
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
