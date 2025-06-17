"""
Main GUI window for the Passcode Generator
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from utils.data_loader import DataLoader
from utils.file_manager import FileManager
from generators.common_generator import CommonGenerator
from generators.date_generator import DateGenerator
from generators.word_generator import WordGenerator
from generators.random_generator import RandomGenerator
from generators.smart_generator import SmartGenerator
from utils.password_filter import PasswordFilter

class PasscodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Passcode Generator")
        self.root.geometry("650x900")
        self.root.resizable(True, True)
        self.exclude_previous = tk.BooleanVar(value=False)
        self.previous_file_path = tk.StringVar(value="")

        # Initialize components
        self.data_loader = DataLoader()
        self.file_manager = FileManager()
        self.password_filter = PasswordFilter()

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

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
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
        title_label = ttk.Label(main_frame, text="Advanced Passcode Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Data files status
        self._setup_status_frame(main_frame, 1)

        # Length settings
        self._setup_length_frame(main_frame, 2)

        # Delimiter settings
        self._setup_delimiter_frame(main_frame, 3)

        # Previous passwords exclusion - NEW
        self._setup_previous_passwords_frame(main_frame, 4)

        # Case variation settings
        self._setup_case_frame(main_frame, 5)

        # Generation method frames
        self._setup_common_frame(main_frame, 6)
        self._setup_combinations_frame(main_frame, 7)
        self._setup_dates_frame(main_frame, 8)
        self._setup_words_frame(main_frame, 9)
        self._setup_random_frame(main_frame, 10)

        # Warning frame
        self._setup_warning_frame(main_frame, 11)

        # Generate button and progress
        self._setup_controls_frame(main_frame, 12)

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

    def _setup_status_frame(self, parent, row):
        """Set up data files status frame"""
        status_frame = ttk.LabelFrame(parent, text="Data Files Status", padding="10")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        files_status = self.data_loader.check_data_files()
        for i, status in enumerate(files_status):
            status_label = ttk.Label(status_frame, text=status, font=("Arial", 8))
            status_label.grid(row=i, column=0, sticky=tk.W)

    def _setup_length_frame(self, parent, row):
        """Set up length settings frame"""
        length_frame = ttk.LabelFrame(parent, text="Passcode Length", padding="10")
        length_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(length_frame, text="Minimum Length:").grid(row=0, column=0, sticky=tk.W)
        min_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.min_length)
        min_spin.grid(row=0, column=1, padx=(10, 0))

        ttk.Label(length_frame, text="Maximum Length:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        max_spin = ttk.Spinbox(length_frame, from_=1, to=50, width=10, 
                              textvariable=self.max_length)
        max_spin.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))

    def _setup_delimiter_frame(self, parent, row):
        """Set up delimiter settings frame"""
        delimiter_frame = ttk.LabelFrame(parent, text="Output Format", padding="10")
        delimiter_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

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

    def _setup_previous_passwords_frame(self, parent, row):
        """Set up previous passwords exclusion frame"""
        previous_frame = ttk.LabelFrame(parent, text="Previous Passwords Exclusion", padding="10")
        previous_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(previous_frame, text="Exclude passwords from previous file", 
                    variable=self.exclude_previous).grid(row=0, column=0, columnspan=3, sticky=tk.W)

        # File selection frame
        file_frame = ttk.Frame(previous_frame)
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="Previous file:").grid(row=0, column=0, sticky=tk.W)

        self.previous_file_entry = ttk.Entry(file_frame, textvariable=self.previous_file_path, 
                                            state="readonly", width=40)
        self.previous_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))

        browse_btn = ttk.Button(file_frame, text="Browse...", command=self._browse_previous_file)
        browse_btn.grid(row=0, column=2, sticky=tk.W)

        clear_btn = ttk.Button(file_frame, text="Clear", command=self._clear_previous_file)
        clear_btn.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))

        # Info label
        info_label = ttk.Label(previous_frame, 
                            text="💡 Supports .txt, .csv, .tsv files. Automatically detects delimiters and removes matching passwords.", 
                            font=("Arial", 8), foreground="gray", wraplength=500)
        info_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # Bind checkbox to enable/disable file selection
        def on_checkbox_change():
            if self.exclude_previous.get():
                self.previous_file_entry.config(state="readonly")
                browse_btn.config(state="normal")
                clear_btn.config(state="normal")
            else:
                self.previous_file_entry.config(state="disabled")
                browse_btn.config(state="disabled")
                clear_btn.config(state="disabled")

        self.exclude_previous.trace_add("write", lambda *args: on_checkbox_change())
        on_checkbox_change()  # Set initial state

    def _browse_previous_file(self):
        """Browse for previous password file"""
        file_path = filedialog.askopenfilename(
            title="Select Previous Password File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("TSV files", "*.tsv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.previous_file_path.set(file_path)
            # Automatically enable the checkbox when file is selected
            self.exclude_previous.set(True)

    def _clear_previous_file(self):
        """Clear the previous file selection"""
        self.previous_file_path.set("")
        self.exclude_previous.set(False)

    def _setup_case_frame(self, parent, row):
        """Set up case variation settings frame"""
        case_frame = ttk.LabelFrame(parent, text="Case Variations", padding="10")
        case_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(case_frame, text="Generate ALL possible upper/lowercase combinations for words", 
                       variable=self.include_case_variations).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        case_info = ttk.Label(case_frame, text="⚠️ WARNING: This will generate MASSIVE wordlists! For 'hello': HeLLo, hELLO, etc.", 
                              font=("Arial", 8), foreground="red", wraplength=500)
        case_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

    def _setup_common_frame(self, parent, row):
        """Set up common passwords frame"""
        common_frame = ttk.LabelFrame(parent, text="Common Passwords & Patterns", padding="10")
        common_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        passwords_count = len(self.data_loader.common_passwords)
        patterns_count = len(self.data_loader.common_patterns)

        ttk.Checkbutton(common_frame, text=f"Include {passwords_count} common passwords and {patterns_count} patterns", 
                       variable=self.include_common).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        info_label = ttk.Label(common_frame, text="Includes: passwords, keyboard patterns, years, number sequences, etc.", 
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

    def _setup_combinations_frame(self, parent, row):
        """Set up smart combinations frame"""
        combo_frame = ttk.LabelFrame(parent, text="Smart Combinations", padding="10")
        combo_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(combo_frame, text="Create intelligent combinations of common passwords + your data", 
                       variable=self.include_combinations).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        passwords_count = len(self.data_loader.common_passwords)
        words_count = len(self.data_loader.common_words)
        combo_info = ttk.Label(combo_frame, text=f"Combines {passwords_count} common passwords with your dates/words + {words_count} common words", 
                              font=("Arial", 8), foreground="gray", wraplength=500)
        combo_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

    def _setup_dates_frame(self, parent, row):
        """Set up dates input frame"""
        dates_frame = ttk.LabelFrame(parent, text="Important Dates", padding="10")
        dates_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(dates_frame, text="Include date-based passcodes", 
                       variable=self.include_dates).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(dates_frame, text="Enter dates (one per line, e.g., 01/15/1990, 2023):").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.dates_text = tk.Text(dates_frame, height=3, width=50)
        self.dates_text.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        dates_scroll = ttk.Scrollbar(dates_frame, orient="vertical", command=self.dates_text.yview)
        dates_scroll.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.dates_text.configure(yscrollcommand=dates_scroll.set)

    def _setup_words_frame(self, parent, row):
        """Set up words input frame"""
        words_frame = ttk.LabelFrame(parent, text="Important Words/Names", padding="10")
        words_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(words_frame, text="Include word-based passcodes", 
                       variable=self.include_words).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(words_frame, text="Enter important words/names (one per line):").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.words_text = tk.Text(words_frame, height=3, width=50)
        self.words_text.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        words_scroll = ttk.Scrollbar(words_frame, orient="vertical", command=self.words_text.yview)
        words_scroll.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.words_text.configure(yscrollcommand=words_scroll.set)

    def _setup_random_frame(self, parent, row):
        """Set up random passcodes frame"""
        random_frame = ttk.LabelFrame(parent, text="Random Passcodes", padding="10")
        random_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(random_frame, text="Include random alphanumeric passcodes", 
                       variable=self.include_random).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Label(random_frame, text="Number of random passcodes:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        random_spin = ttk.Spinbox(random_frame, from_=1, to=100000, width=10, 
                                 textvariable=self.num_random)
        random_spin.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))

    def _setup_warning_frame(self, parent, row):
        """Set up warning frame"""
        warning_frame = ttk.LabelFrame(parent, text="File Size Management", padding="10")
        warning_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        warning_text = ttk.Label(warning_frame, 
                                text="⚠️ Large wordlists will be automatically split into 1GB files\n" +
                                     "🚨 With case variations enabled, expect TENS OF MILLIONS of passcodes!", 
                                font=("Arial", 9), foreground="red", wraplength=500)
        warning_text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

    def _setup_controls_frame(self, parent, row):
        """Set up controls and progress frame"""
        # Generate button
        generate_btn = ttk.Button(parent, text="Generate Passcodes", 
                                 command=self.generate_passcodes, style="Accent.TButton")
        generate_btn.grid(row=row, column=0, columnspan=2, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(parent, text="Ready to generate passcodes")
        self.status_label.grid(row=row+2, column=0, columnspan=2)

    def get_delimiter(self):
        """Get the selected delimiter character(s)"""
        option = self.delimiter_option.get()

        delimiter_map = {
            "newline": "\n",
            "comma": ",",
            "semicolon": ";",
            "tab": "\t",
            "space": " ",
            "pipe": "|"
        }

        if option == "custom":
            custom = self.custom_delimiter.get()
            # Handle escape sequences
            custom = custom.replace("\\n", "\n")
            custom = custom.replace("\\t", "\t")
            custom = custom.replace("\\r", "\r")
            return custom if custom else "\n"  # Default to newline if empty

        return delimiter_map.get(option, "\n")  # Default fallback

    def get_file_extension(self):
        """Get appropriate file extension based on delimiter"""
        option = self.delimiter_option.get()

        if option == "comma":
            return ".csv"
        elif option == "tab":
            return ".tsv"
        else:
            return ".txt"

    def filter_by_length(self, passcodes, min_len, max_len):
        """Filter passcodes by length requirements"""
        return [p for p in passcodes if min_len <= len(p) <= max_len]

    def generate_passcodes(self):
        """Main function to generate all passcodes"""
        try:
            ## Warning for case variations
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

            # Load previous passwords if exclusion is enabled
            previous_passwords = set()
            if self.exclude_previous.get() and self.previous_file_path.get():
                self.password_filter.set_status_callback(lambda msg: self._update_status(msg))
                previous_passwords = self.password_filter.load_previous_passwords(self.previous_file_path.get())

                if previous_passwords:
                    self.status_label.config(text=f"Loaded {len(previous_passwords):,} previous passwords for exclusion")
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

                common_gen = CommonGenerator(self.data_loader, self.include_case_variations.get())
                common_passcodes = common_gen.generate()
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
                    date_gen = DateGenerator(self.data_loader, self.include_case_variations.get())
                    date_combinations = date_gen.generate(date_text)
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

                word_gen = WordGenerator(self.data_loader, self.include_case_variations.get())
                word_gen.set_status_callback(lambda msg: self._update_status(msg))
                word_combinations = word_gen.generate(words)
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

                smart_gen = SmartGenerator(self.data_loader, self.include_case_variations.get())
                smart_combinations = smart_gen.generate(words_text, dates_text)
                filtered_smart = self.filter_by_length(smart_combinations, min_len, max_len)
                all_passcodes.extend(filtered_smart)

                self.status_label.config(text=f"Generated {len(filtered_smart):,} smart combinations")
                self.root.update()

            # Generate random passcodes
            if self.include_random.get():
                self.status_label.config(text="Generating random passcodes...")
                self.root.update()

                random_gen = RandomGenerator()
                random_passcodes = random_gen.generate(self.num_random.get(), min_len, max_len)
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

            # Filter out previous passwords if enabled
            if previous_passwords:
                unique_passcodes = self.password_filter.filter_passwords(unique_passcodes, previous_passwords)

            self.status_label.config(text=f"Generated {len(unique_passcodes):,} unique passcodes")
            self.root.update()

            if not unique_passcodes:
                messagebox.showwarning("Warning", "No new passcodes generated! All passwords were duplicates of previous file.")
                return

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

            self.file_manager.set_status_callback(lambda msg: self._update_status(msg))
            files_created = self.file_manager.save_with_splitting(
                unique_passcodes, base_filename, self.get_delimiter(), self.get_file_extension()
            )

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

    def _update_status(self, message):
        """Update status label and refresh UI"""
        self.status_label.config(text=message)
        self.root.update()

    def _browse_previous_file(self):
        """Browse for previous password file"""
        file_path = filedialog.askopenfilename(
            title="Select Previous Password File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("TSV files", "*.tsv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.previous_file_path.set(file_path)
            # Automatically enable the checkbox when file is selected
            self.exclude_previous.set(True)

            # Show file statistics
            stats = self.password_filter.get_file_stats(file_path)
            if stats:
                file_size_mb = stats['file_size'] / (1024 * 1024)
                messagebox.showinfo("File Statistics", 
                    f"File: {stats['file_name']}\n"
                    f"Size: {file_size_mb:.2f} MB\n"
                    f"Estimated passwords: {stats['password_count']:,}\n\n"
                    f"These passwords will be excluded from new results.")
                
    def _setup_warning_frame(self, parent, row):
        """Set up warning frame"""
        warning_frame = ttk.LabelFrame(parent, text="File Size Management", padding="10")
        warning_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        warning_text = ttk.Label(warning_frame, 
                                text="⚠️ Large wordlists will be automatically split into 1GB files\n" +
                                    "🚨 With case variations enabled, expect TENS OF MILLIONS of passcodes!\n" +
                                    "💡 Previous password exclusion helps avoid generating duplicate wordlists", 
                                font=("Arial", 9), foreground="red", wraplength=500)
        warning_text.grid(row=0, column=0, columnspan=2, sticky=tk.W)

