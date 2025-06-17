"""
Date-based passcode generator
"""

from .base_generator import BaseGenerator
from utils.text_utils import TextUtils

class DateGenerator(BaseGenerator):
    def generate(self, date_text):
        """Generate date-based passcode combinations"""
        combinations = []

        if not date_text.strip():
            return combinations

        dates = TextUtils.parse_dates(date_text)

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
            if self.data_loader:
                for common in self.data_loader.common_passwords[:50]:  # Use top 50 common passwords
                    common_variations = self.get_case_variations(common)

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
