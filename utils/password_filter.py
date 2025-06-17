"""
Password filtering utilities for removing duplicates from previous files
"""

import os
import csv
from typing import Set, List

class PasswordFilter:
    def __init__(self):
        self.status_callback = None

    def set_status_callback(self, callback):
        """Set callback function for status updates"""
        self.status_callback = callback

    def _update_status(self, message):
        """Update status if callback is set"""
        if self.status_callback:
            self.status_callback(message)

    def load_previous_passwords(self, file_path: str) -> Set[str]:
        """Load passwords from a previous file and return as a set"""
        if not file_path or not os.path.exists(file_path):
            return set()

        passwords = set()
        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            self._update_status(f"Loading previous passwords from {os.path.basename(file_path)}...")

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if file_extension == '.csv':
                    passwords.update(self._load_csv_passwords(f))
                elif file_extension == '.tsv':
                    passwords.update(self._load_tsv_passwords(f))
                else:
                    passwords.update(self._load_text_passwords(f))

            self._update_status(f"Loaded {len(passwords):,} previous passwords for exclusion")
            return passwords

        except Exception as e:
            self._update_status(f"Warning: Could not load previous passwords: {str(e)}")
            return set()

    def _load_csv_passwords(self, file_handle) -> Set[str]:
        """Load passwords from CSV file"""
        passwords = set()

        # Try to detect if file has headers
        sample = file_handle.read(1024)
        file_handle.seek(0)

        # Use csv.Sniffer to detect delimiter and quote character
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;')
            reader = csv.reader(file_handle, dialect)
        except:
            # Fallback to comma delimiter
            reader = csv.reader(file_handle, delimiter=',')

        for row_num, row in enumerate(reader):
            if row_num == 0:
                # Check if first row looks like headers
                if self._looks_like_header(row):
                    continue

            # Add all non-empty cells as potential passwords
            for cell in row:
                cell = cell.strip()
                if cell and not self._is_likely_metadata(cell):
                    passwords.add(cell)

        return passwords

    def _load_tsv_passwords(self, file_handle) -> Set[str]:
        """Load passwords from TSV file"""
        passwords = set()
        reader = csv.reader(file_handle, delimiter='\t')

        for row_num, row in enumerate(reader):
            if row_num == 0:
                # Check if first row looks like headers
                if self._looks_like_header(row):
                    continue

            # Add all non-empty cells as potential passwords
            for cell in row:
                cell = cell.strip()
                if cell and not self._is_likely_metadata(cell):
                    passwords.add(cell)

        return passwords

    def _load_text_passwords(self, file_handle) -> Set[str]:
        """Load passwords from text file (one per line or delimited)"""
        passwords = set()

        for line_num, line in enumerate(file_handle):
            line = line.strip()
            if not line:
                continue

            # Try to detect common delimiters
            if any(delimiter in line for delimiter in [',', ';', '\t', '|']):
                # Line contains delimiters, split it
                for delimiter in [',', ';', '\t', '|']:
                    if delimiter in line:
                        parts = line.split(delimiter)
                        for part in parts:
                            part = part.strip()
                            if part and not self._is_likely_metadata(part):
                                passwords.add(part)
                        break
            else:
                # Single password per line
                if not self._is_likely_metadata(line):
                    passwords.add(line)

        return passwords

    def _looks_like_header(self, row: List[str]) -> bool:
        """Check if a row looks like column headers"""
        if not row:
            return False

        header_indicators = [
            'password', 'passwords', 'pass', 'passcode', 'passphrase',
            'username', 'user', 'login', 'email', 'account',
            'id', 'name', 'description', 'type', 'category',
            'strength', 'length', 'created', 'modified'
        ]

        # If any cell contains common header words, likely a header
        for cell in row:
            if cell.lower().strip() in header_indicators:
                return True

        return False

    def _is_likely_metadata(self, text: str) -> bool:
        """Check if text is likely metadata rather than a password"""
        text_lower = text.lower().strip()

        # Skip obvious metadata
        metadata_indicators = [
            'password', 'username', 'email', 'login', 'account',
            'created', 'modified', 'length', 'strength', 'type',
            'id', 'name', 'description', 'category', 'url', 'website'
        ]

        # Skip if it's exactly a metadata word
        if text_lower in metadata_indicators:
            return True

        # Skip if it looks like a date
        if self._looks_like_date(text):
            return True

        # Skip if it's very long (likely not a password)
        if len(text) > 100:
            return True

        return False

    def _looks_like_date(self, text: str) -> bool:
        """Check if text looks like a date"""
        import re

        # Common date patterns
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]

        for pattern in date_patterns:
            if re.match(pattern, text.strip()):
                return True

        return False

    def filter_passwords(self, new_passwords: List[str], previous_passwords: Set[str]) -> List[str]:
        """Filter out passwords that exist in previous set"""
        if not previous_passwords:
            return new_passwords

        self._update_status("Filtering out previous passwords...")

        # Convert to set for faster lookup, then back to list
        new_set = set(new_passwords)
        original_count = len(new_set)

        # Remove passwords that exist in previous set
        filtered_set = new_set - previous_passwords

        filtered_count = len(filtered_set)
        removed_count = original_count - filtered_count

        self._update_status(f"Removed {removed_count:,} duplicate passwords from previous file")

        return list(filtered_set)

    def get_file_stats(self, file_path: str) -> dict:
        """Get statistics about a password file"""
        if not file_path or not os.path.exists(file_path):
            return {}

        try:
            file_size = os.path.getsize(file_path)
            passwords = self.load_previous_passwords(file_path)

            return {
                'file_size': file_size,
                'password_count': len(passwords),
                'file_name': os.path.basename(file_path)
            }
        except:
            return {}
