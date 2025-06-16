import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import itertools
import string
import random
from datetime import datetime
import os

class PasscodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeff's Advanced Passcode Generator")
        self.root.geometry("650x900")
        self.root.resizable(True, True)

        # Variables
        self.min_length = tk.IntVar(value=6)
        self.max_length = tk.IntVar(value=12)
        self.include_dates = tk.BooleanVar(value=True)
        self.include_words = tk.BooleanVar(value=True)
        self.include_random = tk.BooleanVar(value=True)
        self.include_common = tk.BooleanVar(value=True)
        self.include_combinations = tk.BooleanVar(value=True)
        self.include_case_variations = tk.BooleanVar(value=True)
        self.num_random = tk.IntVar(value=100)

        # Delimiter options
        self.delimiter_option = tk.StringVar(value="newline")
        self.custom_delimiter = tk.StringVar(value="")

        # Load data from files
        self.common_passwords = self.load_data_file("common_passwords.txt")
        self.common_patterns = self.load_data_file("common_patterns.txt")
        self.common_words = self.load_data_file("common_words.txt")

        # Special characters and symbols
        self.special_chars = [
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
            "[", "]", "{", "}", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".",
            "?", "/", "~", "`"
        ]

        self.setup_ui()

    def load_data_file(self, filename):
        """Load data from a text file, return list of lines"""
        try:
            # Try to load from same directory as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, filename)

            if not os.path.exists(file_path):
                # Try current working directory
                file_path = filename

            if not os.path.exists(file_path):
                # Try data subdirectory
                data_dir = os.path.join(script_dir, "data")
                file_path = os.path.join(data_dir, filename)

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read lines, strip whitespace, and filter out empty lines
                    lines = [line.strip() for line in f.readlines()]
                    return [line for line in lines if line and not line.startswith('#')]
            else:
                # Return fallback data if file not found
                return self.get_fallback_data(filename)

        except Exception as e:
            print(f"Warning: Could not load {filename}: {e}")
            return self.get_fallback_data(filename)

    def get_fallback_data(self, filename):
        """Return minimal fallback data if files can't be loaded"""
        if filename == "common_passwords.txt":
            return [
                "password", "123456", "password123", "admin", "qwerty", "letmein",
                "welcome", "monkey", "abc123", "111111", "123123", "password1",
                "1234", "12345", "dragon", "master", "hello", "login", "princess"
            ]
        elif filename == "common_patterns.txt":
            return [
                "123", "321", "456", "789", "000", "111", "222", "333", "444", "555",
                "1234", "4321", "2468", "1357", "qwerty", "asdf", "zxcv", "2024", "2023"
            ]
        elif filename == "common_words.txt":
            return [
                "love", "hate", "happy", "sad", "red", "blue", "green", "black", "white",
                "dog", "cat", "bird", "fish", "sun", "moon", "star", "home", "work"
            ]
        return []

    def check_data_files(self):
        """Check if all data files are present and show status"""
        files_status = []
        required_files = ["common_passwords.txt", "common_patterns.txt", "common_words.txt"]

        for filename in required_files:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, filename)

            if not os.path.exists(file_path):
                file_path = filename
            if not os.path.exists(file_path):
                data_dir = os.path.join(script_dir, "data")
                file_path = os.path.join(data_dir, filename)

            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len([line for line in f.readlines() if line.strip() and not line.strip().startswith('#')])
                    files_status.append(f"✅ {filename}: {lines} entries loaded")
                except:
                    files_status.append(f"⚠️ {filename}: Found but error reading")
            else:
                files_status.append(f"❌ {filename}: Not found (using fallback data)")

        return files_status

    def setup_ui(self):
        # Main frame with scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Jeff's Advanced Passcode Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Data files status
        status_frame = ttk.LabelFrame(main_frame, text="Data Files Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        files_status = self.check_data_files()
        for i, status in enumerate(files_status):
            status_label = ttk.Label(status_frame, text=status, font=("Arial", 8))
            status_label.grid(row=i, column=0, sticky=tk.W)

        # Length settings
        length_frame = ttk.LabelFrame(main_frame, text="Passcode Length", padding="10")
        length_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(length_frame, text="Minimum Length:").grid(row=0, column=0, sticky=tk.W)
        min_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.min_length)
        min_spin.grid(row=0, column=1, padx=(10, 0))

        ttk.Label(length_frame, text="Maximum Length:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        max_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.max_length)
        max_spin.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))

        # Delimiter settings
        delimiter_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="10")
        delimiter_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(delimiter_frame, text="Delimiter between passcodes:").grid(row=0, column=0, sticky=tk.W, columnspan=3)

        # Delimiter radio buttons
        ttk.Radiobutton(delimiter_frame, text="New Line (\\n)", variable=self.delimiter_option, 
                       value="newline").grid(row=1, column=0, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(delimiter_frame, text="Comma (,)", variable=self.delimiter_option, 
                       value="comma").grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(delimiter_frame, text="Semicolon (;)", variable=self.delimiter_option, 
                       value="semicolon").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))

        ttk.Radiobutton(delimiter_frame, text="Tab (\\t)", variable=self.delimiter_option, 
                       value="tab").grid(row=2, column=0, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(delimiter_frame, text="Space", variable=self.delimiter_option, 
                       value="space").grid(row=2, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(delimiter_frame, text="Pipe (|)", variable=self.delimiter_option, 
                       value="pipe").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))

        # Custom delimiter option
        custom_frame = ttk.Frame(delimiter_frame)
        custom_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Radiobutton(custom_frame, text="Custom:", variable=self.delimiter_option, 
                       value="custom").grid(row=0, column=0, sticky=tk.W)

        self.custom_entry = ttk.Entry(custom_frame, textvariable=self.custom_delimiter, width=15)
        self.custom_entry.grid(row=0, column=1, padx=(10, 0))

        # Bind custom entry to select custom radio button
        def on_custom_entry_focus(event):
            self.delimiter_option.set("custom")
        self.custom_entry.bind("<FocusIn>", on_custom_entry_focus)
        self.custom_entry.bind("<KeyPress>", on_custom_entry_focus)

        delimiter_info = ttk.Label(delimiter_frame, 
                                  text="💡 Tip: Use \\n for new lines, \\t for tabs, or any custom character(s)", 
                                  font=("Arial", 8), foreground="gray", wraplength=500)
        delimiter_info.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # Case variation settings
        case_frame = ttk.LabelFrame(main_frame, text="Case Variations", padding="10")
        case_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(case_frame, text="Generate ALL possible upper/lowercase combinations for words", 
                       variable=self.include_case_variations).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        case_info = ttk.Label(case_frame, text="⚠️ WARNING: This will generate MASSIVE wordlists! For 'hello': HeLLo, hELLO, etc.", 
                              font=("Arial", 8), foreground="red", wraplength=500)
        case_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Common passwords
        common_frame = ttk.LabelFrame(main_frame, text="Common Passwords & Patterns", padding="10")
        common_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(common_frame, text=f"Include {len(self.common_passwords)} common passwords and {len(self.common_patterns)} patterns", 
                       variable=self.include_common).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        info_label = ttk.Label(common_frame, text="Includes: passwords, keyboard patterns, years, number sequences, etc.", 
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Smart combinations
        combo_frame = ttk.LabelFrame(main_frame, text="Smart Combinations", padding="10")
        combo_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(combo_frame, text="Create intelligent combinations of common passwords + your data", 
                       variable=self.include_combinations).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        combo_info = ttk.Label(combo_frame, text=f"Combines {len(self.common_passwords)} common passwords with your dates/words + {len(self.common_words)} common words", 
                              font=("Arial", 8), foreground="gray", wraplength=500)
        combo_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Important dates
        dates_frame = ttk.LabelFrame(main_frame, text="Important Dates", padding="10")
        dates_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(dates_frame, text="Include date-based passcodes", 
                       variable=self.include_dates).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(dates_frame, text="Enter dates (one per line, e.g., 01/15/1990, 2023):").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.dates_text = tk.Text(dates_frame, height=3, width=50)
        self.dates_text.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        dates_scroll = ttk.Scrollbar(dates_frame, orient="vertical", command=self.dates_text.yview)
        dates_scroll.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.dates_text.configure(yscrollcommand=dates_scroll.set)

        # Important words
        words_frame = ttk.LabelFrame(main_frame, text="Important Words/Names", padding="10")
        words_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(words_frame, text="Include word-based passcodes", 
                       variable=self.include_words).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(words_frame, text="Enter important words/names (one per line):").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.words_text = tk.Text(words_frame, height=3, width=50)
        self.words_text.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        words_scroll = ttk.Scrollbar(words_frame, orient="vertical", command=self.words_text.yview)
        words_scroll.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.words_text.configure(yscrollcommand=words_scroll.set)

        # Random passcodes
        random_frame = ttk.LabelFrame(main_frame, text="Random Passcodes", padding="10")
        random_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(random_frame, text="Include random alphanumeric passcodes", 
                       variable=self.include_random).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(random_frame, text="Number of random passcodes:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        random_spin = ttk.Spinbox(random_frame, from_=1, to=100000, width=10, 
                                 textvariable=self.num_random)
        random_spin.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))

        # File size warning
        warning_frame = ttk.LabelFrame(main_frame, text="File Size Management", padding="10")
        warning_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        warning_text = ttk.Label(warning_frame, 
                                text="⚠️ Large wordlists will be automatically split into 1GB files\n" +
                                     "🚨 With case variations enabled, expect TENS OF MILLIONS of passcodes!", 
                                font=("Arial", 9), foreground="red", wraplength=500)
        warning_text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Passcodes", 
                                 command=self.generate_passcodes, style="Accent.TButton")
        generate_btn.grid(row=11, column=0, columnspan=2, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to generate passcodes")
        self.status_label.grid(row=13, column=0, columnspan=2)

        # Configure scrolling
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def get_delimiter(self):
        """Get the selected delimiter character(s)"""
        option = self.delimiter_option.get()

        if option == "newline":
            return "\n"
        elif option == "comma":
            return ","
        elif option == "semicolon":
            return ";"
        elif option == "tab":
            return "\t"
        elif option == "space":
            return " "
        elif option == "pipe":
            return "|"
        elif option == "custom":
            custom = self.custom_delimiter.get()
            # Handle escape sequences
            custom = custom.replace("\\n", "\n")
            custom = custom.replace("\\t", "\t")
            custom = custom.replace("\\r", "\r")
            return custom if custom else "\n"  # Default to newline if empty
        else:
            return "\n"  # Default fallback

    def get_file_extension(self):
        """Get appropriate file extension based on delimiter"""
        option = self.delimiter_option.get()

        if option == "comma":
            return ".csv"
        elif option == "tab":
            return ".tsv"
        else:
            return ".txt"

    def generate_all_case_variations(self, word):
        """Generate ALL possible upper/lowercase combinations for a word"""
        if not word or not word.isalpha():
            return [word]  # Return original if not all letters

        # Limit to reasonable length to prevent memory explosion
        if len(word) > 10:
            # For very long words, just return basic variations
            return [word, word.lower(), word.upper(), word.capitalize()]

        variations = []
        # Generate all 2^n combinations where n is the length of the word
        for i in range(2 ** len(word)):
            variation = ""
            for j, char in enumerate(word):
                if char.isalpha():
                    # Check if bit j is set in i
                    if (i >> j) & 1:
                        variation += char.upper()
                    else:
                        variation += char.lower()
                else:
                    variation += char
            variations.append(variation)

        return list(set(variations))  # Remove duplicates

    def generate_basic_case_variations(self, word):
        """Generate basic case variations (original method)"""
        return [word, word.lower(), word.upper(), word.capitalize()]

    def parse_dates(self, date_text):
        """Parse dates from text input and return various formats"""
        dates = []
        lines = date_text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to extract numbers from the date
            numbers = ''.join(filter(str.isdigit, line))
            if numbers:
                dates.append(numbers)

                # Add variations
                if len(numbers) >= 4:
                    # Add year if present
                    year = numbers[-4:]
                    dates.append(year)
                    dates.append(year[-2:])  # Last 2 digits of year

                    # Add first 4 digits
                    dates.append(numbers[:4])

                    # Add middle parts
                    if len(numbers) >= 6:
                        dates.append(numbers[2:6])  # Middle 4 digits
                        dates.append(numbers[:2])   # First 2 digits
                        dates.append(numbers[-2:])  # Last 2 digits

                    # Add more variations for longer dates
                    if len(numbers) >= 8:
                        dates.append(numbers[:6])   # First 6 digits
                        dates.append(numbers[2:])   # Skip first 2 digits
                        dates.append(numbers[:-2])  # Skip last 2 digits

        return list(set(dates))  # Remove duplicates

    def generate_word_combinations(self, words):
        """Generate combinations of words with numbers and variations"""
        combinations = []

        # Add common words to user words
        all_words = words + self.common_words

        for word in all_words:
            word = word.strip()
            if not word:
                continue

            # Generate case variations based on setting
            if self.include_case_variations.get():
                variations = self.generate_all_case_variations(word)
                self.status_label.config(text=f"Generating case variations for '{word}': {len(variations)} combinations")
                self.root.update()
            else:
                variations = self.generate_basic_case_variations(word)

            combinations.extend(variations)

            # Add word with common patterns
            for pattern in self.common_patterns:
                for variation in variations:
                    combinations.extend([
                        variation + pattern,
                        pattern + variation,
                        variation + pattern + "!",
                        variation + pattern + "@",
                        variation + "_" + pattern,
                        pattern + "_" + variation
                    ])

            # Add word with special characters (limit to prevent explosion)
            for char in self.special_chars[:10]:  # Use first 10 special chars
                for variation in variations:
                    combinations.extend([
                        variation + char,
                        char + variation,
                        variation + char + "1",
                        variation + "1" + char,
                        variation + char + char,
                        char + variation + char
                    ])

            # Add leetspeak variations
            leet_word = self.to_leetspeak(word)
            if leet_word != word:
                if self.include_case_variations.get():
                    leet_variations = self.generate_all_case_variations(leet_word)
                else:
                    leet_variations = self.generate_basic_case_variations(leet_word)
                combinations.extend(leet_variations)

        return combinations

    def to_leetspeak(self, word):
        """Convert word to leetspeak"""
        leet_map = {
            'a': '4', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '1',
            'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7',
            'l': '1', 'L': '1', 'g': '9', 'G': '9'
        }
        return ''.join(leet_map.get(char, char) for char in word)

    def generate_date_combinations(self, dates):
        """Generate date-based passcode combinations"""
        combinations = []

        for date in dates:
            combinations.append(date)

            # Add with common prefixes/suffixes
            prefixes = ['', 'pass', 'pwd', 'code', 'user', 'admin', 'login', 'key', 'secret']
            suffixes = ['', '!', '@', '#', '$', '*', '123', 'abc', '321', '456', '789', 'xyz']

            for prefix in prefixes:
                for suffix in suffixes:
                    if prefix or suffix:
                        combo = prefix + date + suffix
                        combinations.append(combo)

            # Combine with common passwords (with case variations if enabled)
            for common in self.common_passwords[:50]:  # Use top 50 common passwords
                if self.include_case_variations.get():
                    common_variations = self.generate_all_case_variations(common)
                else:
                    common_variations = self.generate_basic_case_variations(common)

                for common_var in common_variations:
                    combinations.extend([
                        common_var + date,
                        date + common_var,
                        common_var + date + "!",
                        date + common_var + "!",
                        common_var + "_" + date,
                        date + "_" + common_var
                    ])

            # Add reversed dates
            reversed_date = date[::-1]
            combinations.append(reversed_date)

            # Add date with special characters between digits
            if len(date) >= 4:
                for char in ['-', '_', '.', '/']:
                    if len(date) == 8:  # DDMMYYYY or MMDDYYYY
                        combinations.extend([
                            date[:2] + char + date[2:4] + char + date[4:],
                            date[:4] + char + date[4:],
                            date[4:] + char + date[:4]
                        ])
                    elif len(date) == 6:  # DDMMYY or MMDDYY
                        combinations.extend([
                            date[:2] + char + date[2:4] + char + date[4:],
                            date[:4] + char + date[4:]
                        ])

        return combinations

    def generate_smart_combinations(self, user_words, user_dates):
        """Generate intelligent combinations of common passwords with user data"""
        combinations = []

        # Parse user data
        words = []
        if user_words:
            words = [w.strip() for w in user_words.strip().split('\n') if w.strip()]

        dates = []
        if user_dates:
            dates = self.parse_dates(user_dates)

        # All words (user + common)
        all_words = words + self.common_words

        # Combine common passwords with user words
        for word in all_words[:50]:  # Limit to prevent explosion
            if self.include_case_variations.get():
                word_variations = self.generate_all_case_variations(word)
            else:
                word_variations = self.generate_basic_case_variations(word)

            for common in self.common_passwords[:30]:  # Limit common passwords too
                if self.include_case_variations.get():
                    common_variations = self.generate_all_case_variations(common)
                else:
                    common_variations = self.generate_basic_case_variations(common)

                for word_var in word_variations:
                    for common_var in common_variations:
                        combinations.extend([
                            common_var + word_var,
                            word_var + common_var,
                            common_var + word_var + "!",
                            word_var + common_var + "!",
                            common_var + word_var + "123",
                            word_var + common_var + "123",
                            common_var + "_" + word_var,
                            word_var + "_" + common_var,
                            common_var + "." + word_var,
                            word_var + "." + common_var,
                            common_var + word_var + "@",
                            word_var + common_var + "@"
                        ])

        # Combine common passwords with user dates
        for date in dates:
            for common in self.common_passwords[:30]:
                if self.include_case_variations.get():
                    common_variations = self.generate_all_case_variations(common)
                else:
                    common_variations = self.generate_basic_case_variations(common)

                for common_var in common_variations:
                    combinations.extend([
                        common_var + date,
                        date + common_var,
                        common_var + date + "!",
                        date + common_var + "!",
                        common_var + "_" + date,
                        date + "_" + common_var,
                        common_var + "." + date,
                        date + "." + common_var,
                        common_var + date + "@",
                        date + common_var + "@",
                        common_var + date + "#",
                        date + common_var + "#"
                    ])

        # Combine user words with user dates
        for word in words:
            if self.include_case_variations.get():
                word_variations = self.generate_all_case_variations(word)
            else:
                word_variations = self.generate_basic_case_variations(word)

            for date in dates:
                for word_var in word_variations:
                    combinations.extend([
                        word_var + date,
                        date + word_var,
                        word_var + date + "!",
                        date + word_var + "!",
                        word_var + "_" + date,
                        date + "_" + word_var,
                        word_var + date + "@",
                        date + word_var + "@",
                        word_var + "." + date,
                        date + "." + word_var
                    ])

        # Pattern combinations
        for pattern in self.common_patterns[:30]:
            for word in words[:10]:
                if self.include_case_variations.get():
                    word_variations = self.generate_all_case_variations(word)
                else:
                    word_variations = self.generate_basic_case_variations(word)

                for word_var in word_variations:
                    combinations.extend([
                        word_var + pattern,
                        pattern + word_var,
                        word_var + pattern + "!",
                        pattern + word_var + "!"
                    ])

        return combinations

    def generate_common_passwords(self):
        """Generate variations of common passwords"""
        combinations = []

        # Add base common passwords with case variations
        for password in self.common_passwords:
            if self.include_case_variations.get():
                password_variations = self.generate_all_case_variations(password)
            else:
                password_variations = self.generate_basic_case_variations(password)
            combinations.extend(password_variations)

        # Add common passwords with patterns
        for password in self.common_passwords[:50]:  # Limit to prevent explosion
            if self.include_case_variations.get():
                password_variations = self.generate_all_case_variations(password)
            else:
                password_variations = self.generate_basic_case_variations(password)

            for pattern in self.common_patterns[:30]:
                for password_var in password_variations:
                    combinations.extend([
                        password_var + pattern,
                        pattern + password_var,
                        password_var + pattern + "!",
                        password_var + "!" + pattern,
                        password_var + "_" + pattern,
                        pattern + "_" + password_var,
                        password_var + "." + pattern,
                        pattern + "." + password_var
                    ])

        # Add common passwords with special characters
        for password in self.common_passwords[:30]:  # Further limit
            if self.include_case_variations.get():
                password_variations = self.generate_all_case_variations(password)
            else:
                password_variations = self.generate_basic_case_variations(password)

            for char in self.special_chars[:10]:
                for password_var in password_variations:
                    combinations.extend([
                        password_var + char,
                        char + password_var,
                        password_var + char + char,
                        char + password_var + char
                    ])

        # Add common words with patterns
        for word in self.common_words[:50]:  # Limit common words
            if self.include_case_variations.get():
                word_variations = self.generate_all_case_variations(word)
            else:
                word_variations = self.generate_basic_case_variations(word)

            for pattern in self.common_patterns[:20]:
                for word_var in word_variations:
                    combinations.extend([
                        word_var + pattern,
                        pattern + word_var,
                        word_var + pattern + "!",
                        pattern + word_var + "!"
                    ])

        # Add leetspeak versions
        for password in self.common_passwords[:20]:
            leet_password = self.to_leetspeak(password)
            if leet_password != password:
                if self.include_case_variations.get():
                    leet_variations = self.generate_all_case_variations(leet_password)
                else:
                    leet_variations = self.generate_basic_case_variations(leet_password)
                combinations.extend(leet_variations)

        return combinations

    def generate_random_passcodes(self, count, min_len, max_len):
        """Generate random alphanumeric passcodes"""
        characters = string.ascii_letters + string.digits
        passcodes = []

        for _ in range(count):
            length = random.randint(min_len, max_len)
            passcode = ''.join(random.choice(characters) for _ in range(length))
            passcodes.append(passcode)

        return passcodes

    def filter_by_length(self, passcodes, min_len, max_len):
        """Filter passcodes by length requirements"""
        return [p for p in passcodes if min_len <= len(p) <= max_len]

    def save_passcodes_with_splitting(self, passcodes, base_filename):
        """Save passcodes to files, splitting if larger than 1GB"""
        max_file_size = 1024 * 1024 * 1024  # 1GB in bytes
        file_count = 1
        current_size = 0
        current_file = None
        files_created = []
        delimiter = self.get_delimiter()

        try:
            # Create first file
            if len(passcodes) > 1000000:  # If more than 1M passcodes, expect multiple files
                filename = f"{base_filename}_part{file_count}{self.get_file_extension()}"
            else:
                filename = f"{base_filename}{self.get_file_extension()}"

            current_file = open(filename, 'w', encoding='utf-8')
            files_created.append(filename)

            for i, passcode in enumerate(passcodes):
                # Use delimiter instead of always newline
                if i == len(passcodes) - 1:  # Last item
                    line = passcode  # No delimiter after last item
                else:
                    line = passcode + delimiter

                line_size = len(line.encode('utf-8'))

                # Check if adding this line would exceed 1GB
                if current_size + line_size > max_file_size and current_size > 0:
                    # Close current file and start new one
                    current_file.close()
                    file_count += 1
                    filename = f"{base_filename}_part{file_count}{self.get_file_extension()}"
                    current_file = open(filename, 'w', encoding='utf-8')
                    files_created.append(filename)
                    current_size = 0

                current_file.write(line)
                current_size += line_size

                # Update progress every 10000 lines
                if i % 10000 == 0:
                    self.status_label.config(text=f"Writing passcode {i+1:,} of {len(passcodes):,}...")
                    self.root.update()

            if current_file:
                current_file.close()

            return files_created

        except Exception as e:
            if current_file:
                current_file.close()
            # Clean up any files that were created
            for file in files_created:
                try:
                    os.remove(file)
                except:
                    pass
            raise e

    def generate_passcodes(self):
        """Main function to generate all passcodes"""
        try:
            # Warning for case variations
            if self.include_case_variations.get():
                result = messagebox.askyesno("Warning", 
                    "⚠️ You have enabled ALL case variations!\n\n" +
                    "This will generate MASSIVE wordlists that could be:\n" +
                    "• Tens of millions of passcodes\n" +
                    "• Multiple gigabytes in size\n" +
                    "• Take a very long time to generate\n\n" +
                    "Are you sure you want to continue?")
                if not result:
                    return

            self.progress.start()
            self.status_label.config(text="Initializing generation...")
            self.root.update()

            all_passcodes = []
            min_len = self.min_length.get()
            max_len = self.max_length.get()

            if min_len > max_len:
                messagebox.showerror("Error", "Minimum length cannot be greater than maximum length!")
                return

            # Generate common passwords
            if self.include_common.get():
                self.status_label.config(text="Generating common passwords and patterns...")
                self.root.update()
                common_passcodes = self.generate_common_passwords()
                filtered_common = self.filter_by_length(common_passcodes, min_len, max_len)
                all_passcodes.extend(filtered_common)
                self.status_label.config(text=f"Generated {len(filtered_common):,} common password variations")
                self.root.update()

            # Generate date-based passcodes
            if self.include_dates.get():
                self.status_label.config(text="Generating date-based passcodes...")
                self.root.update()
                date_text = self.dates_text.get("1.0", tk.END)
                if date_text.strip():
                    dates = self.parse_dates(date_text)
                    date_combinations = self.generate_date_combinations(dates)
                    filtered_dates = self.filter_by_length(date_combinations, min_len, max_len)
                    all_passcodes.extend(filtered_dates)
                    self.status_label.config(text=f"Generated {len(filtered_dates):,} date-based passcodes")
                    self.root.update()

            # Generate word-based passcodes
            if self.include_words.get():
                self.status_label.config(text="Generating word-based passcodes...")
                self.root.update()
                words_text = self.words_text.get("1.0", tk.END)
                words = []
                if words_text.strip():
                    words = words_text.strip().split('\n')
                word_combinations = self.generate_word_combinations(words)
                filtered_words = self.filter_by_length(word_combinations, min_len, max_len)
                all_passcodes.extend(filtered_words)
                self.status_label.config(text=f"Generated {len(filtered_words):,} word-based passcodes")
                self.root.update()

            # Generate smart combinations
            if self.include_combinations.get():
                self.status_label.config(text="Generating smart combinations...")
                self.root.update()
                words_text = self.words_text.get("1.0", tk.END)
                dates_text = self.dates_text.get("1.0", tk.END)
                smart_combinations = self.generate_smart_combinations(words_text, dates_text)
                filtered_smart = self.filter_by_length(smart_combinations, min_len, max_len)
                all_passcodes.extend(filtered_smart)
                self.status_label.config(text=f"Generated {len(filtered_smart):,} smart combinations")
                self.root.update()

            # Generate random passcodes
            if self.include_random.get():
                self.status_label.config(text="Generating random passcodes...")
                self.root.update()
                random_passcodes = self.generate_random_passcodes(self.num_random.get(), min_len, max_len)
                all_passcodes.extend(random_passcodes)
                self.status_label.config(text=f"Generated {len(random_passcodes):,} random passcodes")
                self.root.update()

            if not all_passcodes:
                messagebox.showwarning("Warning", "No passcodes generated! Please select at least one generation method.")
                return

            # Remove duplicates
            self.status_label.config(text="Removing duplicates...")
            self.root.update()
            unique_passcodes = list(set(all_passcodes))

            self.status_label.config(text=f"Generated {len(unique_passcodes):,} unique passcodes")
            self.root.update()

            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=self.get_file_extension(),
                filetypes=[
                    ("Text files", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("TSV files", "*.tsv"),
                    ("All files", "*.*")
                ],
                title="Save Passcode List"
            )

            if not file_path:
                return

            # Remove extension from file_path for base filename
            base_filename = os.path.splitext(file_path)[0]

            # Save passcodes with splitting
            self.status_label.config(text="Saving passcodes...")
            self.root.update()

            files_created = self.save_passcodes_with_splitting(unique_passcodes, base_filename)

            self.progress.stop()

            # Show completion message
            if len(files_created) == 1:
                message = f"Successfully generated {len(unique_passcodes):,} passcodes!\n\nSaved to: {files_created[0]}"
            else:
                message = f"Successfully generated {len(unique_passcodes):,} passcodes!\n\nSaved to {len(files_created)} files:\n"
                for file in files_created:
                    message += f"• {os.path.basename(file)}\n"

            messagebox.showinfo("Success", message)
            self.status_label.config(text=f"Completed! Generated {len(unique_passcodes):,} unique passcodes")

        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error occurred during generation")

def main():
    root = tk.Tk()
    app = PasscodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
