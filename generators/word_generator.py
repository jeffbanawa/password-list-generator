"""
Word-based passcode generator
"""

from .base_generator import BaseGenerator
from utils.text_utils import TextUtils

class WordGenerator(BaseGenerator):
    def __init__(self, data_loader=None, use_case_variations=False):
        super().__init__(data_loader, use_case_variations)
        self.status_callback = None

    def set_status_callback(self, callback):
        """Set callback function for status updates"""
        self.status_callback = callback

    def _update_status(self, message):
        """Update status if callback is set"""
        if self.status_callback:
            self.status_callback(message)

    def generate(self, user_words):
        """Generate combinations of words with numbers and variations"""
        combinations = []

        # Add common words to user words
        all_words = user_words + (self.data_loader.common_words if self.data_loader else [])

        for word in all_words:
            word = word.strip()
            if not word:
                continue

            # Generate case variations based on setting
            variations = self.get_case_variations(word)
            if self.use_case_variations:
                self._update_status(f"Generating case variations for '{word}': {len(variations)} combinations")

            combinations.extend(variations)

            # Add word with common patterns
            if self.data_loader:
                for pattern in self.data_loader.common_patterns:
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
            leet_word = TextUtils.to_leetspeak(word)
            if leet_word != word:
                leet_variations = self.get_case_variations(leet_word)
                combinations.extend(leet_variations)

        return combinations
