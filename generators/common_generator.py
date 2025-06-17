"""
Common passwords and patterns generator
"""

from .base_generator import BaseGenerator
from utils.text_utils import TextUtils

class CommonGenerator(BaseGenerator):
    def generate(self):
        """Generate variations of common passwords"""
        combinations = []

        if not self.data_loader:
            return combinations

        # Add base common passwords with case variations
        for password in self.data_loader.common_passwords:
            password_variations = self.get_case_variations(password)
            combinations.extend(password_variations)

        # Add common passwords with patterns
        for password in self.data_loader.common_passwords[:50]:  # Limit to prevent explosion
            password_variations = self.get_case_variations(password)

            for pattern in self.data_loader.common_patterns[:30]:
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
        for password in self.data_loader.common_passwords[:30]:  # Further limit
            password_variations = self.get_case_variations(password)

            for char in self.special_chars[:10]:
                for password_var in password_variations:
                    combinations.extend([
                        password_var + char,
                        char + password_var,
                        password_var + char + char,
                        char + password_var + char
                    ])

        # Add common words with patterns
        for word in self.data_loader.common_words[:50]:  # Limit common words
            word_variations = self.get_case_variations(word)

            for pattern in self.data_loader.common_patterns[:20]:
                for word_var in word_variations:
                    combinations.extend([
                        word_var + pattern,
                        pattern + word_var,
                        word_var + pattern + "!",
                        pattern + word_var + "!"
                    ])

        # Add leetspeak versions
        for password in self.data_loader.common_passwords[:20]:
            leet_password = TextUtils.to_leetspeak(password)
            if leet_password != password:
                leet_variations = self.get_case_variations(leet_password)
                combinations.extend(leet_variations)

        return combinations
