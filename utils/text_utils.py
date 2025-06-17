"""
Text processing utilities
"""

class TextUtils:
    @staticmethod
    def generate_all_case_variations(word):
        """Generate ALL possible upper/lowercase combinations for a word"""
        if not word or not word.isalpha():
            return [word]  # Return original if not all letters

        # Limit to reasonable length to prevent memory explosion
        if len(word) > 10:
            # For very long words, just return basic variations
            return TextUtils.generate_basic_case_variations(word)

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

    @staticmethod
    def generate_basic_case_variations(word):
        """Generate basic case variations"""
        return [word, word.lower(), word.upper(), word.capitalize()]

    @staticmethod
    def to_leetspeak(word):
        """Convert word to leetspeak"""
        leet_map = {
            'a': '4', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '1',
            'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7',
            'l': '1', 'L': '1', 'g': '9', 'G': '9'
        }
        return ''.join(leet_map.get(char, char) for char in word)

    @staticmethod
    def parse_dates(date_text):
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
