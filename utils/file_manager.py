"""
File management utilities for saving and splitting large files
"""

import os

class FileManager:
    def __init__(self):
        self.status_callback = None

    def set_status_callback(self, callback):
        """Set callback function for status updates"""
        self.status_callback = callback

    def _update_status(self, message):
        """Update status if callback is set"""
        if self.status_callback:
            self.status_callback(message)

    def save_with_splitting(self, passcodes, base_filename, delimiter, file_extension):
        """Save passcodes to files, splitting if larger than 1GB"""
        max_file_size = 1024 * 1024 * 1024  # 1GB in bytes
        file_count = 1
        current_size = 0
        current_file = None
        files_created = []

        try:
            # Create first file
            if len(passcodes) > 1000000:  # If more than 1M passcodes, expect multiple files
                filename = f"{base_filename}_part{file_count}{file_extension}"
            else:
                filename = f"{base_filename}{file_extension}"

            current_file = open(filename, 'w', encoding='utf-8')
            files_created.append(filename)

            for i, passcode in enumerate(passcodes):
                # Use delimiter instead of always newline
                if i == len(passcodes) - 1:  # Last item
                    line = passcode  # No delimiter after last item
                else:
                    line = passcode + delimiter

                line_size = len(line.encode('utf-8'))

                # Check if adding this line would exceed 1GB
                if current_size + line_size > max_file_size and current_size > 0:
                    # Close current file and start new one
                    current_file.close()
                    file_count += 1
                    filename = f"{base_filename}_part{file_count}{file_extension}"
                    current_file = open(filename, 'w', encoding='utf-8')
                    files_created.append(filename)
                    current_size = 0

                current_file.write(line)
                current_size += line_size

                # Update progress every 10000 lines
                if i % 10000 == 0:
                    self._update_status(f"Writing passcode {i+1:,} of {len(passcodes):,}...")

            if current_file:
                current_file.close()

            return files_created

        except Exception as e:
            if current_file:
                current_file.close()
            # Clean up any files that were created
            for file in files_created:
                try:
                    os.remove(file)
                except:
                    pass
            raise e
