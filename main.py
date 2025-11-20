# Simple Wordlist Generator
# This program generates password combinations from user input

import itertools
import os

def get_user_words():
    """Get words from user until they want to stop"""
    words = []
    print("\n=== Enter Words for Wordlist ===")
    print("Enter words one by one (type 'done' to finish)")
    
    while True:
        word = input("Enter word: ")
        if word.lower() == 'done':
            break
        if word:  # only add non-empty words
            words.append(word)
            print(f"Added: {word}")
    
    return words

def get_variations(word):
    """Create simple variations of a word"""
    variations = []
    
    # original word
    variations.append(word)
    
    # uppercase first letter
    variations.append(word.capitalize())
    
    # all uppercase
    variations.append(word.upper())
    
    # all lowercase
    variations.append(word.lower())
    
    return variations

def calculate_combinations(words):
    """Calculate total possible combinations"""
    # Get all variations for each word
    all_variations = []
    for word in words:
        variations = get_variations(word)
        all_variations.append(variations)
    
    # Calculate combinations
    # Each word can be any of its variations
    total = 1
    for variations in all_variations:
        total = total * len(variations)
    
    # Also count combinations with common numbers
    numbers = ['', '123', '1234', '2024', '2025', '123456', '!', '@', '#']
    total = total * len(numbers)
    
    return total

def generate_wordlist(words, count):
    """Generate wordlist with specified count"""
    print("\nGenerating wordlist...")
    
    # Create variations for each word
    all_variations = []
    for word in words:
        variations = get_variations(word)
        all_variations.append(variations)
    
    # Common additions
    additions = ['', '123', '1234', '2024', '2025', '123456', '!', '@', '#']
    
    # Generate combinations
    generated = []
    generated_count = 0
    
    # Use nested loops to generate combinations
    for combo in itertools.product(*all_variations):
        for addition in additions:
            # Combine all words and add number/symbol
            password = ''.join(combo) + addition
            generated.append(password)
            generated_count += 1
            
            # Show progress every 10000 passwords
            if generated_count % 10000 == 0:
                print(f"Generated: {generated_count} passwords...")
            
            # Stop if we reached the count
            if generated_count >= count:
                return generated
    
    return generated

def save_wordlist(wordlist, filename):
    """Save wordlist to file"""
    # Make sure directory exists
    if not os.path.exists('wordlist_files'):
        os.makedirs('wordlist_files')
    
    filepath = os.path.join('wordlist_files', filename)
    
    print(f"\nSaving to {filepath}...")
    
    # Write to file
    with open(filepath, 'w') as file:
        for password in wordlist:
            file.write(password + '\n')
    
    print(f"Saved {len(wordlist)} passwords to {filepath}")

def main():
    """Main function"""
    print("=" * 50)
    print("   WORDLIST GENERATOR")
    print("=" * 50)
    
    # Get words from user
    words = get_user_words()
    
    if len(words) == 0:
        print("\nNo words entered. Exiting...")
        return
    
    print(f"\nYou entered {len(words)} words: {', '.join(words)}")
    
    # Calculate possible combinations
    total_combinations = calculate_combinations(words)
    print(f"\nTotal possible combinations: {total_combinations:,}")
    
    # Ask how many user wants
    while True:
        try:
            count = int(input("\nHow many passwords do you want to generate? "))
            if count <= 0:
                print("Please enter a positive number")
                continue
            if count > total_combinations:
                print(f"Maximum available is {total_combinations:,}")
                count = total_combinations
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Generate wordlist
    wordlist = generate_wordlist(words, count)
    
    # Save to file
    filename = input("\nEnter filename (without .txt): ") + ".txt"
    save_wordlist(wordlist, filename)
    
    print("\n" + "=" * 50)
    print("Done! Check the wordlist_files folder")
    print("=" * 50)

# Run the program
if __name__ == "__main__":
    main()
