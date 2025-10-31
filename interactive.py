"""
Interactive CLI UI for AI OSINT Wordlist Generator
Cross-platform (Windows & Linux) with beautiful interface
"""

import os
import sys
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# ANSI color codes (work on Windows 10+ and Linux)
class Colors:
    # Enable ANSI colors on Windows
    if platform.system() == 'Windows':
        os.system('color')
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class UI:
    """Beautiful cross-platform CLI UI"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    @staticmethod
    def print_header():
        """Print the main header"""
        UI.clear_screen()
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("╔═════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                         ║")
        print("║     🔥  SOCIAL ENGINEERING WORDLIST GENERATOR  🔥                      ║")
        print("║                                                                         ║")
        print("║     Pure OSINT + Pattern Mutations | Security Research Tool            ║")
        print("║                                                                         ║")
        print("╚═════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
    
    @staticmethod
    def print_banner():
        """Print ASCII art banner"""
        banner = f"""{Colors.BRIGHT_MAGENTA}
    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ██╗███████╗████████╗
    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██║██╔════╝╚══██╔══╝
    ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     ██║███████╗   ██║   
    ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██║╚════██║   ██║   
    ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║███████║   ██║   
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚══════╝   ╚═╝   
    {Colors.BRIGHT_CYAN}           G E N E R A T O R{Colors.RESET}
        """
        print(banner)
    
    @staticmethod
    def print_box(text: str, color=Colors.CYAN, width=75):
        """Print text in a box"""
        print(f"\n{color}┌{'─' * (width - 2)}┐")
        print(f"│ {text:<{width - 4}} │")
        print(f"└{'─' * (width - 2)}┘{Colors.RESET}\n")
    
    @staticmethod
    def print_menu_item(number: str, title: str, description: str, icon: str = ""):
        """Print a menu item"""
        print(f"{Colors.BRIGHT_YELLOW}  [{number}]{Colors.RESET} {icon} {Colors.BOLD}{title}{Colors.RESET}")
        print(f"      {Colors.DIM}{description}{Colors.RESET}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"\n{Colors.BRIGHT_GREEN}✓{Colors.RESET} {Colors.GREEN}{message}{Colors.RESET}\n")
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"\n{Colors.BRIGHT_RED}✗{Colors.RESET} {Colors.RED}{message}{Colors.RESET}\n")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(f"\n{Colors.BRIGHT_YELLOW}⚠{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}\n")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"\n{Colors.BRIGHT_CYAN}ℹ{Colors.RESET} {Colors.CYAN}{message}{Colors.RESET}\n")
    
    @staticmethod
    def print_progress(current: int, total: int, message: str = ""):
        """Print progress bar"""
        percentage = (current / total) * 100
        filled = int(percentage / 2)
        bar = '█' * filled + '░' * (50 - filled)
        
        print(f"\r{Colors.BRIGHT_CYAN}[{bar}]{Colors.RESET} {percentage:.1f}% {message}", end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    @staticmethod
    def get_input(prompt: str, color=Colors.BRIGHT_CYAN) -> str:
        """Get user input with colored prompt"""
        return input(f"{color}➤ {Colors.RESET}{prompt}: ").strip()
    
    @staticmethod
    def wait_for_enter():
        """Wait for user to press Enter"""
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
    
    @staticmethod
    def print_separator(char="─", width=75):
        """Print a separator line"""
        print(f"{Colors.DIM}{char * width}{Colors.RESET}")


class MenuSystem:
    """Interactive menu system"""
    
    def __init__(self):
        self.running = True
    
    def show_main_menu(self):
        """Display the main menu"""
        UI.print_header()
        UI.print_banner()
        
        print(f"{Colors.BRIGHT_WHITE}Select Generation Mode:{Colors.RESET}\n")
        
        UI.print_menu_item("1", "Quick Generate", "Fast wordlist with manual keywords", "⚡")
        UI.print_menu_item("2", "Company OSINT", "Target company-based wordlist", "🏢")
        UI.print_menu_item("3", "Username OSINT", "Target username-based wordlist", "👤")
        UI.print_menu_item("4", "Load from File", "Use existing wordlist file", "📄")
        UI.print_menu_item("5", "Advanced Mode", "Combine multiple sources", "🔬")
        UI.print_menu_item("6", "View Output", "Show generated wordlists", "📂")
        UI.print_menu_item("7", "View Examples", "Show example commands", "📖")
        UI.print_menu_item("8", "About", "About this tool", "ℹ️")
        UI.print_menu_item("0", "Exit", "Quit the application", "🚪")
        
        UI.print_separator()
        
        choice = UI.get_input("Enter your choice [0-8]")
        return choice
    
    def quick_generate(self):
        """Quick generate mode"""
        UI.clear_screen()
        UI.print_box("⚡ QUICK GENERATE MODE", Colors.BRIGHT_YELLOW)
        
        print(f"{Colors.BRIGHT_WHITE}Enter your keywords (one per line):{Colors.RESET}")
        print(f"{Colors.DIM}Press Enter after each keyword{Colors.RESET}")
        print(f"{Colors.DIM}Press Ctrl+D (Linux) or Ctrl+Z then Enter (Windows) when done{Colors.RESET}\n")
        
        keywords = []
        keyword_num = 1
        
        try:
            while True:
                keyword = input(f"{Colors.CYAN}Keyword {keyword_num}:{Colors.RESET} ").strip()
                if keyword:
                    keywords.append(keyword)
                    keyword_num += 1
        except (EOFError, KeyboardInterrupt):
            # User pressed Ctrl+D or Ctrl+Z
            pass
        
        if not keywords:
            UI.print_error("No keywords provided!")
            UI.wait_for_enter()
            return
        
        # Join keywords with comma
        words = ','.join(keywords)
        
        print(f"\n{Colors.BRIGHT_GREEN}✓ Collected {len(keywords)} keyword(s){Colors.RESET}")
        print(f"{Colors.DIM}Keywords: {', '.join(keywords[:5])}{' ...' if len(keywords) > 5 else ''}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_WHITE}How many passwords to generate?{Colors.RESET}")
        print(f"{Colors.DIM}Recommended: 100-1000 for quick tests{Colors.RESET}\n")
        
        count = UI.get_input("Count")
        
        try:
            count = int(count)
            if count < 100 or count > 1000000:
                UI.print_warning("Count adjusted to valid range (100-1,000,000)")
                count = max(100, min(count, 1000000))
        except ValueError:
            UI.print_error("Invalid count! Using default: 1000")
            count = 1000
        
        # Get output filename
        print(f"\n{Colors.BRIGHT_WHITE}Output filename:{Colors.RESET}")
        print(f"{Colors.DIM}Leave empty for auto-generated name (optional){Colors.RESET}\n")
        
        output_file = UI.get_input("Filename")
        
        # Auto-add .txt extension if not present
        if output_file:
            if not output_file.endswith('.txt'):
                output_file = output_file + '.txt'
            # Save to output folder
            output_file = f"output/{output_file}"
        
        # Build command
        main_py = SCRIPT_DIR / "main.py"
        cmd = f'cd "{SCRIPT_DIR}" && python "{main_py}" --words "{words}" --count {count}'
        if output_file:
            cmd += f' --output "{output_file}"'
        
        UI.print_info(f"Generating {count:,} passwords from {len(keywords)} keyword(s)...")
        
        print(f"\n{Colors.BRIGHT_GREEN}Starting generation...{Colors.RESET}\n")
        UI.print_separator("═")
        
        os.system(cmd)
        
        print(f"\n{Colors.BRIGHT_GREEN}═══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        UI.wait_for_enter()
    
    def company_osint(self):
        """Company OSINT mode"""
        UI.clear_screen()
        UI.print_box("🏢 COMPANY OSINT MODE", Colors.BRIGHT_BLUE)
        
        print(f"{Colors.BRIGHT_WHITE}Target Company Information:{Colors.RESET}\n")
        
        company = UI.get_input("Company name")
        
        if not company:
            UI.print_error("Company name required!")
            UI.wait_for_enter()
            return
        
        print(f"\n{Colors.BRIGHT_WHITE}Company website (optional):{Colors.RESET}")
        print(f"{Colors.DIM}Example: https://example.com{Colors.RESET}\n")
        
        website = UI.get_input("Website URL (press Enter to skip)")
        
        print(f"\n{Colors.BRIGHT_WHITE}How many passwords to generate?{Colors.RESET}\n")
        count = UI.get_input("Count (default: 1000)")
        
        try:
            count = int(count) if count else 1000
        except ValueError:
            count = 1000
        
        # Build command
        main_py = SCRIPT_DIR / "main.py"
        cmd = f'cd "{SCRIPT_DIR}" && python "{main_py}" --company "{company}" --count {count}'
        if website:
            cmd += f' --website "{website}"'
        
        UI.print_info(f"Running command...")
        
        print(f"\n{Colors.BRIGHT_GREEN}Starting OSINT collection and generation...{Colors.RESET}\n")
        UI.print_separator("═")
        
        os.system(cmd)
        
        print(f"\n{Colors.BRIGHT_GREEN}═══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        UI.wait_for_enter()
    
    def username_osint(self):
        """Username OSINT mode"""
        UI.clear_screen()
        UI.print_box("👤 USERNAME OSINT MODE", Colors.BRIGHT_MAGENTA)
        
        print(f"{Colors.BRIGHT_WHITE}Target Username:{Colors.RESET}")
        print(f"{Colors.DIM}Will search across 15+ social media platforms{Colors.RESET}\n")
        
        username = UI.get_input("Username")
        
        if not username:
            UI.print_error("Username required!")
            UI.wait_for_enter()
            return
        
        print(f"\n{Colors.BRIGHT_WHITE}How many passwords to generate?{Colors.RESET}\n")
        count = UI.get_input("Count (default: 500)")
        
        try:
            count = int(count) if count else 500
        except ValueError:
            count = 500
        
        # Build command
        main_py = SCRIPT_DIR / "main.py"
        cmd = f'cd "{SCRIPT_DIR}" && python "{main_py}" --username "{username}" --count {count}'
        
        UI.print_info(f"Running command...")
        
        print(f"\n{Colors.BRIGHT_GREEN}Starting username search and generation...{Colors.RESET}\n")
        UI.print_separator("═")
        
        os.system(cmd)
        
        print(f"\n{Colors.BRIGHT_GREEN}═══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        UI.wait_for_enter()
    
    def load_from_file(self):
        """Load from file mode"""
        UI.clear_screen()
        UI.print_box("📄 LOAD FROM FILE MODE", Colors.BRIGHT_CYAN)
        
        print(f"{Colors.BRIGHT_WHITE}Wordlist file path:{Colors.RESET}")
        print(f"{Colors.DIM}Example: examples/base_wordlist.txt{Colors.RESET}\n")
        
        filepath = UI.get_input("File path")
        
        if not filepath:
            UI.print_error("File path required!")
            UI.wait_for_enter()
            return
        
        if not os.path.exists(filepath):
            UI.print_error(f"File not found: {filepath}")
            UI.wait_for_enter()
            return
        
        print(f"\n{Colors.BRIGHT_WHITE}How many passwords to generate?{Colors.RESET}\n")
        count = UI.get_input("Count (default: 5000)")
        
        try:
            count = int(count) if count else 5000
        except ValueError:
            count = 5000
        
        # Build command
        main_py = SCRIPT_DIR / "main.py"
        cmd = f'cd "{SCRIPT_DIR}" && python "{main_py}" --wordlist "{filepath}" --count {count}'
        
        UI.print_info(f"Running command...")
        
        print(f"\n{Colors.BRIGHT_GREEN}Starting generation from file...{Colors.RESET}\n")
        UI.print_separator("═")
        
        os.system(cmd)
        
        print(f"\n{Colors.BRIGHT_GREEN}═══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        UI.wait_for_enter()
    
    def advanced_mode(self):
        """Advanced mode - combine multiple sources"""
        UI.clear_screen()
        UI.print_box("🔬 ADVANCED MODE - COMBINE SOURCES", Colors.BRIGHT_RED)
        
        print(f"{Colors.BRIGHT_WHITE}Combine multiple intelligence sources:{Colors.RESET}\n")
        
        sources = {}
        
        # Company
        print(f"{Colors.CYAN}Company name (press Enter to skip):{Colors.RESET}")
        company = UI.get_input("Company")
        if company:
            sources['company'] = company
            website = UI.get_input("  Website URL (optional)")
            if website:
                sources['website'] = website
        
        # Username
        print(f"\n{Colors.CYAN}Username (press Enter to skip):{Colors.RESET}")
        username = UI.get_input("Username")
        if username:
            sources['username'] = username
        
        # Words
        print(f"\n{Colors.CYAN}Manual keywords (press Enter to skip):{Colors.RESET}")
        words = UI.get_input("Keywords")
        if words:
            sources['words'] = words
        
        # Wordlist file
        print(f"\n{Colors.CYAN}Wordlist file (press Enter to skip):{Colors.RESET}")
        wordlist = UI.get_input("File path")
        if wordlist and os.path.exists(wordlist):
            sources['wordlist'] = wordlist
        
        if not sources:
            UI.print_error("No sources provided!")
            UI.wait_for_enter()
            return
        
        print(f"\n{Colors.BRIGHT_WHITE}How many passwords to generate?{Colors.RESET}\n")
        count = UI.get_input("Count (default: 10000)")
        
        try:
            count = int(count) if count else 10000
        except ValueError:
            count = 10000
        
        # Build command
        main_py = SCRIPT_DIR / "main.py"
        cmd = f'cd "{SCRIPT_DIR}" && python "{main_py}" --count {count}'
        
        if 'company' in sources:
            cmd += f' --company "{sources["company"]}"'
            if 'website' in sources:
                cmd += f' --website "{sources["website"]}"'
        
        if 'username' in sources:
            cmd += f' --username "{sources["username"]}"'
        
        if 'words' in sources:
            cmd += f' --words "{sources["words"]}"'
        
        if 'wordlist' in sources:
            cmd += f' --wordlist "{sources["wordlist"]}"'
        
        output = UI.get_input("\nOutput filename (optional)")
        if output:
            cmd += f' --output "{output}"'
        
        UI.print_info(f"Running command...")
        
        print(f"\n{Colors.BRIGHT_GREEN}Starting comprehensive generation...{Colors.RESET}\n")
        UI.print_separator("═")
        
        os.system(cmd)
        
        print(f"\n{Colors.BRIGHT_GREEN}═══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        UI.wait_for_enter()
    
    def view_output(self):
        """View generated wordlists"""
        UI.clear_screen()
        UI.print_box("📂 GENERATED WORDLISTS", Colors.BRIGHT_GREEN)
        
        output_dir = Path('output')
        if not output_dir.exists():
            UI.print_error("Output directory not found!")
            UI.wait_for_enter()
            return
        
        wordlists = list(output_dir.glob('*.txt'))
        
        if not wordlists:
            UI.print_warning("No wordlists generated yet!")
            UI.wait_for_enter()
            return
        
        print(f"{Colors.BRIGHT_WHITE}Found {len(wordlists)} wordlist(s):{Colors.RESET}\n")
        
        for i, file in enumerate(sorted(wordlists, reverse=True)[:10], 1):
            size_kb = file.stat().st_size / 1024
            modified = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            print(f"{Colors.CYAN}{i}.{Colors.RESET} {file.name}")
            print(f"   Size: {size_kb:.2f} KB | Modified: {modified}\n")
        
        if len(wordlists) > 10:
            print(f"{Colors.DIM}... and {len(wordlists) - 10} more{Colors.RESET}\n")
        
        print(f"{Colors.DIM}Location: {output_dir.absolute()}{Colors.RESET}")
        
        UI.wait_for_enter()
    
    def show_examples(self):
        """Show examples"""
        UI.clear_screen()
        UI.print_box("📖 EXAMPLE COMMANDS", Colors.BRIGHT_MAGENTA)
        
        examples = [
            ("Quick Test", 'python main.py --words "password,admin" --count 100'),
            ("Company", 'python main.py --company "TechCorp" --count 1000'),
            ("Username", 'python main.py --username john_doe --count 500'),
            ("From File", 'python main.py --wordlist base.txt --count 5000'),
            ("Advanced", 'python main.py --company "Corp" --username admin --count 10000'),
        ]
        
        for title, cmd in examples:
            print(f"{Colors.BRIGHT_YELLOW}▸ {title}:{Colors.RESET}")
            print(f"  {Colors.DIM}{cmd}{Colors.RESET}\n")
        
        UI.wait_for_enter()
    
    def show_about(self):
        """Show about information"""
        UI.clear_screen()
        UI.print_box("ℹ️ ABOUT", Colors.BRIGHT_CYAN)
        
        about_text = f"""
{Colors.BRIGHT_WHITE}Social Engineering Wordlist Generator{Colors.RESET}
{Colors.DIM}Version 2.0.0{Colors.RESET}

{Colors.CYAN}Description:{Colors.RESET}
  A pure OSINT-based wordlist generator that uses social engineering
  techniques and pattern-based mutations to generate contextual passwords.
  No AI or API required!

{Colors.CYAN}Features:{Colors.RESET}
  • Company data scraping
  • Username OSINT (15+ platforms)
  • Pattern-based mutations (leet speak, numbers, special chars)
  • Scalable (100 to 1,000,000 passwords)
  • 100% offline capable

{Colors.CYAN}Platform:{Colors.RESET}
  • Windows & Linux compatible
  • Python 3.8+
  • No API keys needed

{Colors.YELLOW}⚠️  For authorized security testing only!{Colors.RESET}

{Colors.DIM}Created for educational and authorized penetration testing{Colors.RESET}
        """
        
        print(about_text)
        UI.wait_for_enter()
    
    def run(self):
        """Main menu loop"""
        while self.running:
            try:
                choice = self.show_main_menu()
                
                if choice == '1':
                    self.quick_generate()
                elif choice == '2':
                    self.company_osint()
                elif choice == '3':
                    self.username_osint()
                elif choice == '4':
                    self.load_from_file()
                elif choice == '5':
                    self.advanced_mode()
                elif choice == '6':
                    self.view_output()
                elif choice == '7':
                    self.show_examples()
                elif choice == '8':
                    self.show_about()
                elif choice == '0':
                    UI.clear_screen()
                    print(f"\n{Colors.BRIGHT_CYAN}Thank you for using AI OSINT Wordlist Generator!{Colors.RESET}")
                    print(f"{Colors.DIM}Stay ethical, stay legal! 🛡️{Colors.RESET}\n")
                    self.running = False
                else:
                    UI.print_error("Invalid choice! Please select 0-8.")
                    UI.wait_for_enter()
            
            except KeyboardInterrupt:
                UI.clear_screen()
                print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}\n")
                self.running = False
            
            except Exception as e:
                UI.print_error(f"An error occurred: {e}")
                UI.wait_for_enter()


def main():
    """Main entry point"""
    try:
        menu = MenuSystem()
        menu.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Goodbye!{Colors.RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
