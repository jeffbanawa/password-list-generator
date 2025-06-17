"""
Base generator class with common functionality
"""

from utils.text_utils import TextUtils

class BaseGenerator:
    def __init__(self, data_loader=None, use_case_variations=False):
        self.data_loader = data_loader
        self.use_case_variations = use_case_variations
        self.special_chars = [
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
            "[", "]", "{", "}", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".",
            "?", "/", "~", "`"
        ]

    def get_case_variations(self, word):
        """Get case variations based on settings"""
        if self.use_case_variations:
            return TextUtils.generate_all_case_variations(word)
        else:
            return TextUtils.generate_basic_case_variations(word)

    def generate(self, *args, **kwargs):
        """Override in subclasses"""
        raise NotImplementedError("Subclasses must implement generate method")
