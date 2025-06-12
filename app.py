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
        self.root.geometry("650x800")
        self.root.resizable(True, True)

        # Variables
        self.min_length = tk.IntVar(value=6)
        self.max_length = tk.IntVar(value=12)
        self.include_dates = tk.BooleanVar(value=True)
        self.include_words = tk.BooleanVar(value=True)
        self.include_random = tk.BooleanVar(value=True)
        self.include_common = tk.BooleanVar(value=True)
        self.include_combinations = tk.BooleanVar(value=True)
        self.num_random = tk.IntVar(value=100)

        # Expanded common passwords (200+ most common)
        self.common_passwords = [
            # Top 100 most common passwords
            "password", "123456", "password123", "admin", "qwerty", "letmein",
            "welcome", "monkey", "1234567890", "abc123", "111111", "123123",
            "password1", "1234", "12345", "dragon", "master", "hello",
            "login", "princess", "solo", "qwerty123", "starwars", "whatever",
            "trustno1", "batman", "passw0rd", "zaq12wsx", "Password1", "football",
            "baseball", "welcome123", "ninja", "mustang", "access", "shadow",
            "jordan", "superman", "test", "guest", "123456789", "000000",
            "qwertyuiop", "696969", "hottie", "freedom", "aa123456", "qazwsx",
            "loveme", "fuckyou", "123qwe", "hello123", "lovely", "babygirl",
            "michael", "ashley", "654321", "jesus", "password12", "computer",

            # Additional 100+ common passwords
            "iloveyou", "charlie", "sunshine", "1q2w3e4r", "princess1", "555555",
            "lovely1", "7777777", "888888", "123321", "daniel", "qwerty1",
            "tiger", "1990", "justin", "chocolate", "banana", "joshua",
            "bubble", "lakers", "playboy", "hunter", "jennifer", "buster",
            "soccer", "harley", "batman1", "andrew", "tigger", "sunshine1",
            "password2", "ginger", "charlie1", "orange", "chicken", "rainbow",
            "jordan23", "liverpool", "blink182", "asdfgh", "winter", "dolphin",
            "bigdog", "murphy", "banana1", "mickey", "greenday", "chocolate1",
            "jessica", "pepper", "1111", "summer", "internet", "service",
            "canada", "hello1", "hunter1", "welcome1", "biteme", "hannah",
            "hockey", "angels", "maggie", "skittles", "emma", "joshua1",
            "madison", "guitar", "muffin", "cooper", "cookie", "chocolate2",
            "icecream", "golfing", "richard", "george", "charles", "money",
            "tinkerbell", "beautiful", "coolman", "tiger1", "batman2", "rock",
            "ginger1", "hammer", "summer1", "swimming", "cooper1", "nascar",
            "redskins", "miller", "shooter", "picture", "united", "cookie1",
            "lucky", "hotdog", "salasana", "scooter", "blue", "dallas",
            "cowboys", "eagles", "chicken1", "bear", "smoothie", "apple",
            "canada1", "sniper", "panther", "tiger123", "fire", "great"
        ]

        # Expanded patterns (numbers, keyboard patterns, etc.)
        self.common_patterns = [
            # Basic number patterns
            "123", "321", "456", "789", "000", "111", "222", "333", "444", "555",
            "666", "777", "888", "999", "12", "21", "34", "43", "56", "65",
            "78", "87", "90", "09", "01", "10", "11", "22", "33", "99",

            # Extended number patterns
            "1234", "4321", "2468", "1357", "9876", "5678", "8765", "1111",
            "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999",
            "0000", "1212", "2121", "3434", "4343", "5656", "6565", "7878",
            "8787", "9090", "0909", "1010", "2020", "3030", "4040", "5050",

            # Years and dates
            "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017",
            "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009",
            "2008", "2007", "2006", "2005", "2000", "1999", "1998", "1997",
            "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989",
            "1988", "1987", "1986", "1985", "1984", "1983", "1982", "1981",
            "1980", "1979", "1978", "1977", "1976", "1975", "1970", "1969",

            # Short years
            "24", "23", "22", "21", "20", "19", "18", "17", "16", "15",
            "14", "13", "12", "11", "10", "09", "08", "07", "06", "05",
            "00", "99", "98", "97", "96", "95", "94", "93", "92", "91",
            "90", "89", "88", "87", "86", "85", "84", "83", "82", "81",
            "80", "79", "78", "77", "76", "75", "70", "69",

            # Keyboard patterns
            "qwe", "asd", "zxc", "qaz", "wsx", "edc", "rfv", "tgb", "yhn",
            "ujm", "ik", "ol", "p", "mnb", "vcx", "dfg", "hjk", "rty",
            "uio", "sdf", "ghj", "klz", "xcv", "bnm", "poi", "lkj",
            "qwer", "asdf", "zxcv", "tyui", "ghjk", "bnmq", "wert", "sdfg",
            "xcvb", "yuio", "hjkl", "vbnm", "erty", "dfgh", "cvbn", "rtyu",
            "fghj", "vbnm", "tyuio", "ghjkl", "cvbnm", "qwerty", "asdfgh",
            "zxcvbn", "qwertyui", "asdfghjk", "zxcvbnm"
        ]

        # Expanded common words (300+ words)
        self.common_words = [
            # Emotions and relationships
            "love", "hate", "happy", "sad", "angry", "joy", "peace", "hope",
            "dream", "wish", "heart", "soul", "mind", "life", "death",
            "friend", "family", "mother", "father", "sister", "brother",
            "wife", "husband", "girlfriend", "boyfriend", "baby", "child",

            # Colors
            "red", "blue", "green", "yellow", "black", "white", "pink",
            "purple", "orange", "brown", "gray", "silver", "gold",

            # Animals
            "dog", "cat", "bird", "fish", "horse", "cow", "pig", "sheep",
            "lion", "tiger", "bear", "wolf", "fox", "rabbit", "mouse",
            "elephant", "monkey", "snake", "frog", "turtle", "shark",
            "eagle", "hawk", "owl", "duck", "chicken", "turkey",

            # Nature
            "sun", "moon", "star", "sky", "earth", "fire", "water", "wind",
            "rain", "snow", "ice", "tree", "flower", "grass", "mountain",
            "ocean", "river", "lake", "beach", "forest", "desert", "island",

            # Food and drinks
            "pizza", "burger", "cake", "cookie", "bread", "cheese", "milk",
            "coffee", "tea", "beer", "wine", "water", "juice", "soda",
            "chocolate", "candy", "sugar", "honey", "apple", "banana",
            "orange", "grape", "strawberry", "cherry", "lemon", "potato",

            # Technology and internet
            "computer", "internet", "email", "phone", "mobile", "laptop",
            "tablet", "website", "google", "facebook", "twitter", "youtube",
            "instagram", "snapchat", "tiktok", "netflix", "amazon", "apple",
            "microsoft", "windows", "android", "iphone", "samsung", "wifi",

            # Common objects
            "house", "home", "car", "bike", "boat", "plane", "train", "bus",
            "door", "window", "table", "chair", "bed", "book", "pen", "paper",
            "money", "dollar", "euro", "pound", "gold", "silver", "diamond",
            "key", "lock", "safe", "box", "bag", "shoe", "hat", "shirt",

            # Sports and games
            "football", "soccer", "basketball", "baseball", "tennis", "golf",
            "hockey", "swimming", "running", "boxing", "wrestling", "racing",
            "game", "play", "win", "lose", "team", "player", "coach", "ball",
            "goal", "score", "match", "tournament", "champion", "victory",

            # Work and education
            "work", "job", "office", "boss", "employee", "manager", "teacher",
            "student", "school", "college", "university", "class", "test",
            "exam", "grade", "homework", "study", "learn", "knowledge",
            "skill", "talent", "career", "business", "company", "meeting",

            # Time and dates
            "time", "day", "night", "morning", "evening", "today", "tomorrow",
            "yesterday", "week", "month", "year", "hour", "minute", "second",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
            "sunday", "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",

            # Places and locations
            "america", "usa", "canada", "mexico", "england", "france", "germany",
            "italy", "spain", "russia", "china", "japan", "india", "australia",
            "brazil", "argentina", "egypt", "africa", "europe", "asia",
            "city", "town", "village", "country", "state", "street", "road",
            "park", "store", "shop", "mall", "restaurant", "hotel", "airport",

            # Abstract concepts
            "god", "heaven", "hell", "angel", "devil", "good", "evil", "right",
            "wrong", "true", "false", "yes", "no", "maybe", "always", "never",
            "forever", "eternity", "infinity", "zero", "one", "first", "last",
            "best", "worst", "big", "small", "hot", "cold", "fast", "slow",

            # Common adjectives
            "beautiful", "ugly", "smart", "stupid", "strong", "weak", "rich",
            "poor", "young", "old", "new", "ancient", "modern", "classic",
            "special", "normal", "weird", "strange", "funny", "serious",
            "cool", "hot", "warm", "cold", "fresh", "stale", "clean", "dirty"
        ]

        # Special characters and symbols
        self.special_chars = [
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
            "[", "]", "{", "}", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".",
            "?", "/", "~", "`"
        ]

        self.setup_ui()

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
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Length settings
        length_frame = ttk.LabelFrame(main_frame, text="Passcode Length", padding="10")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(length_frame, text="Minimum Length:").grid(row=0, column=0, sticky=tk.W)
        min_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.min_length)
        min_spin.grid(row=0, column=1, padx=(10, 0))

        ttk.Label(length_frame, text="Maximum Length:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        max_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.max_length)
        max_spin.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))

        # Common passwords
        common_frame = ttk.LabelFrame(main_frame, text="Common Passwords & Patterns", padding="10")
        common_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(common_frame, text="Include 200+ most common passwords and patterns", 
                       variable=self.include_common).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        info_label = ttk.Label(common_frame, text="Includes: passwords, keyboard patterns, years, number sequences, etc.", 
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Smart combinations
        combo_frame = ttk.LabelFrame(main_frame, text="Smart Combinations", padding="10")
        combo_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(combo_frame, text="Create intelligent combinations of common passwords + your data", 
                       variable=self.include_combinations).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        combo_info = ttk.Label(combo_frame, text="Combines 200+ common passwords with your dates/words + 300+ common words", 
                              font=("Arial", 8), foreground="gray", wraplength=500)
        combo_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Important dates
        dates_frame = ttk.LabelFrame(main_frame, text="Important Dates", padding="10")
        dates_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

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
        words_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

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
        random_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(random_frame, text="Include random alphanumeric passcodes", 
                       variable=self.include_random).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(random_frame, text="Number of random passcodes:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        random_spin = ttk.Spinbox(random_frame, from_=1, to=100000, width=10, 
                                 textvariable=self.num_random)
        random_spin.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))

        # File size warning
        warning_frame = ttk.LabelFrame(main_frame, text="File Size Management", padding="10")
        warning_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        warning_text = ttk.Label(warning_frame, 
                                text="⚠️ Large wordlists will be automatically split into 1GB files\n" +
                                     "With all options enabled, expect millions of passcodes!", 
                                font=("Arial", 9), foreground="orange", wraplength=500)
        warning_text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Passcodes", 
                                 command=self.generate_passcodes, style="Accent.TButton")
        generate_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to generate passcodes")
        self.status_label.grid(row=10, column=0, columnspan=2)

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

            # Add the word itself in different cases
            variations = [word, word.lower(), word.upper(), word.capitalize()]
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

            # Add word with special characters
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
                combinations.extend([leet_word, leet_word.upper(), leet_word.lower()])

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

            # Combine with common passwords
            for common in self.common_passwords[:50]:  # Use top 50 common passwords
                combinations.extend([
                    common + date,
                    date + common,
                    common + date + "!",
                    date + common + "!",
                    common + "_" + date,
                    date + "_" + common
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
        for word in all_words[:100]:  # Limit to prevent explosion
            word_variations = [word, word.lower(), word.upper(), word.capitalize()]
            for common in self.common_passwords:
                for word_var in word_variations:
                    combinations.extend([
                        common + word_var,
                        word_var + common,
                        common + word_var + "!",
                        word_var + common + "!",
                        common + word_var + "123",
                        word_var + common + "123",
                        common + "_" + word_var,
                        word_var + "_" + common,
                        common + "." + word_var,
                        word_var + "." + common,
                        common + word_var + "@",
                        word_var + common + "@"
                    ])

        # Combine common passwords with user dates
        for date in dates:
            for common in self.common_passwords:
                combinations.extend([
                    common + date,
                    date + common,
                    common + date + "!",
                    date + common + "!",
                    common + "_" + date,
                    date + "_" + common,
                    common + "." + date,
                    date + "." + common,
                    common + date + "@",
                    date + common + "@",
                    common + date + "#",
                    date + common + "#"
                ])

        # Combine user words with user dates
        for word in words:
            word_variations = [word, word.lower(), word.upper(), word.capitalize()]
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

        # Triple combinations (common + word + date)
        for word in words[:10]:  # Limit to prevent explosion
            word_var = word.lower()
            for date in dates[:10]:
                for common in self.common_passwords[:20]:
                    combinations.extend([
                        common + word_var + date,
                        word_var + common + date,
                        date + common + word_var,
                        common + date + word_var,
                        word_var + date + common,
                        date + word_var + common
                    ])

        # Pattern combinations
        for pattern in self.common_patterns[:50]:
            for word in words[:20]:
                word_var = word.lower()
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

        # Add base common passwords
        combinations.extend(self.common_passwords)

        # Add common passwords with patterns
        for password in self.common_passwords:
            for pattern in self.common_patterns:
                combinations.extend([
                    password + pattern,
                    pattern + password,
                    password + pattern + "!",
                    password + "!" + pattern,
                    password + "_" + pattern,
                    pattern + "_" + password,
                    password + "." + pattern,
                    pattern + "." + password
                ])

        # Add common passwords with special characters
        for password in self.common_passwords[:50]:  # Limit to prevent explosion
            for char in self.special_chars[:15]:
                combinations.extend([
                    password + char,
                    char + password,
                    password + char + char,
                    char + password + char
                ])

        # Add common words with patterns
        for word in self.common_words:
            for pattern in self.common_patterns[:30]:
                combinations.extend([
                    word + pattern,
                    pattern + word,
                    word.capitalize() + pattern,
                    word.upper() + pattern,
                    pattern + word.capitalize(),
                    pattern + word.upper()
                ])

        # Add leetspeak versions
        for password in self.common_passwords[:30]:
            leet_password = self.to_leetspeak(password)
            if leet_password != password:
                combinations.extend([leet_password, leet_password.upper(), leet_password.lower()])

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

        try:
            # Create first file
            if len(passcodes) > 1:
                filename = f"{base_filename}_part{file_count}.txt"
            else:
                filename = f"{base_filename}.txt"

            current_file = open(filename, 'w', encoding='utf-8')
            files_created.append(filename)

            for i, passcode in enumerate(passcodes):
                line = passcode + '\n'
                line_size = len(line.encode('utf-8'))

                # Check if adding this line would exceed 1GB
                if current_size + line_size > max_file_size and current_size > 0:
                    # Close current file and start new one
                    current_file.close()
                    file_count += 1
                    filename = f"{base_filename}_part{file_count}.txt"
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
                user_words = self.words_text.get("1.0", tk.END)
                user_dates = self.dates_text.get("1.0", tk.END)
                if user_words.strip() or user_dates.strip():
                    smart_combinations = self.generate_smart_combinations(user_words, user_dates)
                    filtered_smart = self.filter_by_length(smart_combinations, min_len, max_len)
                    all_passcodes.extend(filtered_smart)
                    self.status_label.config(text=f"Generated {len(filtered_smart):,} smart combinations")
                    self.root.update()

            # Generate random passcodes
            if self.include_random.get():
                self.status_label.config(text="Generating random passcodes...")
                self.root.update()
                random_passcodes = self.generate_random_passcodes(
                    self.num_random.get(), min_len, max_len)
                all_passcodes.extend(random_passcodes)
                self.status_label.config(text=f"Generated {self.num_random.get():,} random passcodes")
                self.root.update()

            self.status_label.config(text="Removing duplicates...")
            self.root.update()

            # Remove duplicates while preserving order
            unique_passcodes = []
            seen = set()
            for i, passcode in enumerate(all_passcodes):
                if passcode not in seen:
                    unique_passcodes.append(passcode)
                    seen.add(passcode)

                # Update progress every 50000 items
                if i % 50000 == 0:
                    self.status_label.config(text=f"Removing duplicates... {i:,}/{len(all_passcodes):,}")
                    self.root.update()

            if not unique_passcodes:
                messagebox.showwarning("Warning", "No passcodes generated! Please check your settings.")
                return

            # Estimate file size
            estimated_size = sum(len(p.encode('utf-8')) + 1 for p in unique_passcodes)  # +1 for newline
            estimated_size_mb = estimated_size / (1024 * 1024)

            self.status_label.config(text=f"Estimated file size: {estimated_size_mb:.1f} MB")
            self.root.update()

            # Get base filename
            base_filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Passcodes As"
            )

            if base_filename:
                # Remove .txt extension if present for splitting logic
                if base_filename.endswith('.txt'):
                    base_filename = base_filename[:-4]

                self.status_label.config(text="Saving passcodes to file(s)...")
                self.root.update()

                files_created = self.save_passcodes_with_splitting(unique_passcodes, base_filename)

                # Show success message
                if len(files_created) == 1:
                    message = f"Generated {len(unique_passcodes):,} unique passcodes!\nSaved to: {files_created[0]}"
                else:
                    message = f"Generated {len(unique_passcodes):,} unique passcodes!\nSplit into {len(files_created)} files:\n"
                    for file in files_created:
                        file_size = os.path.getsize(file) / (1024 * 1024)
                        message += f"• {os.path.basename(file)} ({file_size:.1f} MB)\n"

                self.status_label.config(text=f"Successfully saved {len(unique_passcodes):,} passcodes to {len(files_created)} file(s)")
                messagebox.showinfo("Success", message)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error occurred during generation")

        finally:
            self.progress.stop()

def main():
    root = tk.Tk()
    app = PasscodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
