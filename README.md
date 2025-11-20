# <p align="center">
#   <img src="https://github.com/InoshMatheesha/WordlistGenarator/blob/main/banner.png" alt="Wordlist Generator banner" style="max-width:100%; height:auto;" />
# </p>

<p align="center">
   <img src="https://github.com/InoshMatheesha/WordlistGenarator/blob/main/icon.png" alt="Wordlist Generator icon" width="64" style="vertical-align:middle; margin-right:12px;" />
   <span style="font-family: 'Courier New', monospace; font-size:30px; font-weight:700; vertical-align:middle;">Wordlist Generator</span>
   <br/>
   <em style="color:#666;">Generate focused offline wordlists for authorized security testing.</em>
</p>

---

A simple Python program that generates custom password wordlists based on user-provided words. Perfect for security testing and password recovery scenarios.

## Why This Project?

This tool was created to help security professionals and ethical hackers generate targeted wordlists for penetration testing. Instead of using massive generic wordlists, you can create smaller, more focused lists based on known information about a target (like names, birthdates, company names, etc.).

**Use Cases:**
- Penetration testing and security audits
- Password recovery for authorized accounts
- Testing password strength in your organization
- Educational purposes to understand password patterns

⚠️ **Important:** This tool is for educational and authorized security testing only. Never use it for unauthorized access to systems.

## Features

- ✅ Generate passwords from multiple input words
- ✅ Creates variations (uppercase, lowercase, capitalized)
- ✅ Combines words in different orders
- ✅ Adds common patterns (123, 2024, !, @, #, etc.)
- ✅ Filter by password length (min/max)
- ✅ Shows possible combinations before generation
- ✅ Progress tracking for large wordlists
- ✅ Removes duplicate passwords automatically
- ✅ Saves output to text files

## Installation

### Windows

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download the program**
   ```bash
   git clone https://github.com/InoshMatheesha/WordlistGenarator.git
   cd WordlistGenarator
   ```

3. **Run the program**
   ```bash
   python main.py
   ```

### Linux

1. **Install Python** (usually pre-installed)
   ```bash
   sudo apt update
   sudo apt install python3
   ```

2. **Download the program**
   ```bash
   git clone https://github.com/InoshMatheesha/WordlistGenarator.git
   cd WordlistGenarator
   ```

3. **Run the program**
   ```bash
   python3 main.py
   ```

## How to Use

1. **Run the program**
   ```bash
   python main.py
   ```

2. **Enter your words**
   - Type words one by one (names, dates, IDs, etc.)
   - Type `done` when finished

3. **Set length range**
   - Enter minimum password length
   - Enter maximum password length

4. **Choose quantity**
   - Program shows how many combinations are possible
   - Enter how many passwords you want to generate

5. **Save the wordlist**
   - Enter a filename
   - File will be saved in `wordlist_files/` folder

## Example Usage

```
=== Enter Words for Wordlist ===
Enter words one by one (type 'done' to finish)
Enter word: john
Added: john
Enter word: smith
Added: smith
Enter word: 1990
Added: 1990
Enter word: done

You entered 3 words: john, smith, 1990

Possible combinations (ALL): 3,456

Minimum password length: 6
Maximum password length: 15

Calculating combinations with length filter...
Possible combinations (length 6-15): 1,248

How many passwords do you want to generate? 1000

Generating wordlist...
Generated: 1000 passwords...

Enter filename (without .txt): johnsmith
Saved 1000 passwords to wordlist_files/johnsmith.txt

Done! Check the wordlist_files folder
```

## Sample Output

The generated wordlist will contain variations like:
```
john123
JOHN1990
smith!
johnsmith
Smith1990
1990john
JohnSmith2024
john@
...
```

## Requirements

- Python 3.6 or higher
- No external libraries needed (uses only built-in modules)

## Project Structure

```
WordlistGenarator/
├── main.py              # Main program file
├── README.md            # This file
└── wordlist_files/      # Generated wordlists stored here
```

## Technical Details

The program generates passwords by:
1. Creating variations (lowercase, UPPERCASE, Capitalized)
2. Combining 1, 2, or all words in different orders
3. Adding common suffixes (numbers and symbols)
4. Filtering by length requirements
5. Removing duplicates

## Legal Disclaimer

This tool is provided for educational and authorized security testing purposes only. Users must:
- Have explicit permission to test target systems
- Comply with all applicable laws and regulations
- Use responsibly and ethically

The author is not responsible for any misuse of this tool.

## Author

Created by Inosh Matheesha

## License

Free to use for educational purposes.

---

**Note:** Always ensure you have proper authorization before conducting any security testing or password recovery activities.
