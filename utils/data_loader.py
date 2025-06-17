"""
Data file loading utilities
"""

import os

class DataLoader:
    def __init__(self):
        self.common_passwords = self.load_data_file("common_passwords.txt")
        self.common_patterns = self.load_data_file("common_patterns.txt")
        self.common_words = self.load_data_file("common_words.txt")

    def load_data_file(self, filename):
        """Load data from a text file, return list of lines"""
        try:
            # Try to load from same directory as script
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
