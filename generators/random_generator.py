"""
Random passcode generator
"""

import string
import random
from .base_generator import BaseGenerator

class RandomGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()

    def generate(self, count, min_len, max_len):
        """Generate random alphanumeric passcodes"""
        characters = string.ascii_letters + string.digits
        passcodes = []

        for _ in range(count):
            length = random.randint(min_len, max_len)
            passcode = ''.join(random.choice(characters) for _ in range(length))
            passcodes.append(passcode)

        return passcodes
