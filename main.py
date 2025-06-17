#!/usr/bin/env python3
"""
Advanced Passcode Generator
Main application entry point
"""

import tkinter as tk
from gui.main_window import PasscodeGeneratorGUI

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PasscodeGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
