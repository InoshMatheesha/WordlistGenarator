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
    
    # Calculate combinations for each word
    total_per_order = 1
    for variations in all_variations:
        total_per_order = total_per_order * len(variations)
    
    # Multiply by number of different orders (permutations)
    num_words = len(words)
    num_orders = 1
    for i in range(1, num_words + 1):
        num_orders = num_orders * i  # factorial
    
    total = total_per_order * num_orders
    
    # Also count combinations with common numbers
    numbers = ['', '123', '1234', '2024', '2025', '123456', '!', '@', '#']
    total = total * len(numbers)
    
    return total

def count_filtered_combinations(words, min_length, max_length):
    """Count combinations that match length filter"""
    # Get all variations for each word
    all_variations = []
    for word in words:
        variations = get_variations(word)
        all_variations.append(variations)
    
    # Common additions
    additions = ['', '123', '1234', '2024', '2025', '123456', '!', '@', '#']
    
    # Count matching combinations
    count = 0
    
    # Check all permutations of words (different orders)
    for perm in itertools.permutations(range(len(words))):
        # Get variations for this order
        ordered_variations = [all_variations[i] for i in perm]
        
        # Count combinations with this order
        for combo in itertools.product(*ordered_variations):
            for addition in additions:
                # Combine all words and add number/symbol
                password = ''.join(combo) + addition
                
                # Check if password length is in range
                password_length = len(password)
                if password_length >= min_length and password_length <= max_length:
                    count = count + 1
    
    return count

def generate_wordlist(words, count, min_length, max_length):
    """Generate wordlist with specified count and length filter"""
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
    
    # Generate all permutations of words (different orders)
    for perm in itertools.permutations(range(len(words))):
        # Get variations for this order
        ordered_variations = [all_variations[i] for i in perm]
        
        # Generate combinations with this order
        for combo in itertools.product(*ordered_variations):
            for addition in additions:
                # Combine all words and add number/symbol
                password = ''.join(combo) + addition
                
                # Check if password length is in range
                password_length = len(password)
                if password_length >= min_length and password_length <= max_length:
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
    
    # Ask for password length range
    while True:
        try:
            min_length = int(input("\nMinimum password length: "))
            max_length = int(input("Maximum password length: "))
            if min_length <= 0 or max_length <= 0:
                print("Length must be positive")
                continue
            if min_length > max_length:
                print("Minimum length cannot be greater than maximum")
                continue
            break
        except ValueError:
            print("Please enter valid numbers")
    
    # Calculate filtered combinations
    print("\nCalculating combinations with length filter...")
    filtered_count = count_filtered_combinations(words, min_length, max_length)
    print(f"Possible combinations (length {min_length}-{max_length}): {filtered_count:,}")
    
    # Adjust count if needed
    if count > filtered_count:
        print(f"Adjusting to maximum available: {filtered_count:,}")
        count = filtered_count
    
    # Generate wordlist
    wordlist = generate_wordlist(words, count, min_length, max_length)
    
    # Save to file
    filename = input("\nEnter filename (without .txt): ") + ".txt"
    save_wordlist(wordlist, filename)
    
    print("\n" + "=" * 50)
    print("Done! Check the wordlist_files folder")
    print("=" * 50)

# Run the program
if __name__ == "__main__":
    main()
