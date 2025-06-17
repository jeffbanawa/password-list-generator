"""
Smart combinations generator
"""

from .base_generator import BaseGenerator
from utils.text_utils import TextUtils

class SmartGenerator(BaseGenerator):
    def generate(self, user_words_text, user_dates_text):
        """Generate intelligent combinations of common passwords with user data"""
        combinations = []

        if not self.data_loader:
            return combinations

        # Parse user data
        words = []
        if user_words_text:
            words = [w.strip() for w in user_words_text.strip().split('\n') if w.strip()]

        dates = []
        if user_dates_text:
            dates = TextUtils.parse_dates(user_dates_text)

        # All words (user + common)
        all_words = words + self.data_loader.common_words

        # Combine common passwords with user words
        for word in all_words[:50]:  # Limit to prevent explosion
            word_variations = self.get_case_variations(word)

            for common in self.data_loader.common_passwords[:30]:  # Limit common passwords too
                common_variations = self.get_case_variations(common)

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
            for common in self.data_loader.common_passwords[:30]:
                common_variations = self.get_case_variations(common)

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
            word_variations = self.get_case_variations(word)

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
        for pattern in self.data_loader.common_patterns[:30]:
            for word in words[:10]:
                word_variations = self.get_case_variations(word)

                for word_var in word_variations:
                    combinations.extend([
                        word_var + pattern,
                        pattern + word_var,
                        word_var + pattern + "!",
                        pattern + word_var + "!"
                    ])

        return combinations
