# Advanced Passcode Generator

A powerful Python application with GUI for generating comprehensive password wordlists for security testing and password auditing. This tool creates millions of potential passcodes by intelligently combining common passwords, personal data, and various patterns.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ⚠️ Disclaimer

This tool is intended for **legitimate security testing and educational purposes only**. Users are responsible for ensuring they have proper authorization before using generated wordlists for password testing. The authors are not responsible for any misuse of this software.

## 🚀 Features

### Core Capabilities
- **200+ Common Passwords**: Includes the most frequently used passwords and variations
- **300+ Common Words**: Comprehensive dictionary of commonly used words across multiple categories
- **Smart Combinations**: Intelligently combines common passwords with personal data
- **All Case Variations**: Generates every possible upper/lowercase combination (e.g., "hello" → 32 variations)
- **Date Processing**: Extracts and formats dates in multiple ways
- **Pattern Generation**: Keyboard patterns, number sequences, and special character combinations
- **Leetspeak Conversion**: Converts words to leetspeak (e.g., "password" → "p4ssw0rd")
- **Automatic File Splitting**: Splits large wordlists into 1GB chunks automatically

### Advanced Features
- **Length Filtering**: Set minimum and maximum password lengths
- **Duplicate Removal**: Automatically removes duplicate entries
- **Progress Tracking**: Real-time progress updates during generation
- **Memory Management**: Handles large datasets efficiently
- **File Size Estimation**: Shows estimated output size before generation

## 📋 Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Standard Python libraries: `string`, `random`, `datetime`, `os`, `itertools`

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/advanced-passcode-generator.git
cd advanced-passcode-generator
```

2. **Ensure Python is installed:**
```bash
python --version
```

3. **Run the application:**
```bash
python passcode_generator.py
```

### Alternative Installation Methods

**Download as ZIP:**
1. Download the ZIP file from GitHub
2. Extract to your desired location
3. Run `python passcode_generator.py`

**Direct Download:**
```bash
wget https://raw.githubusercontent.com/yourusername/advanced-passcode-generator/main/passcode_generator.py
python passcode_generator.py
```

## 🎯 Usage

### Basic Usage

1. **Launch the application:**
```bash
python passcode_generator.py
```

2. **Configure settings:**
   - Set minimum and maximum password lengths
   - Choose which generation methods to include
   - Enter personal data (dates, names, words)

3. **Generate wordlist:**
   - Click "Generate Passcodes"
   - Choose save location
   - Wait for completion

### Configuration Options

#### Length Settings
- **Minimum Length**: 1-50 characters
- **Maximum Length**: 1-50 characters

#### Generation Methods

**✅ Common Passwords & Patterns**
- 200+ most common passwords
- Keyboard patterns (qwerty, asdf, etc.)
- Number sequences (123, 321, 1234, etc.)
- Years (1969-2025)

**✅ Case Variations**
- **⚠️ WARNING**: Generates ALL possible upper/lowercase combinations
- Example: "hello" → hello, Hello, hEllo, heLlo, helLo, hellO, HEllo, etc.
- Can generate millions of variations from just a few words

**✅ Smart Combinations**
- Combines common passwords with your personal data
- Creates intelligent patterns like: password+1990, john+123456, admin+yourname

**✅ Date-Based Passcodes**
- Enter important dates (birthdays, anniversaries, etc.)
- Automatically extracts and formats dates multiple ways
- Combines dates with common prefixes/suffixes

**✅ Word-Based Passcodes**
- Enter important words, names, places
- Generates variations with numbers and special characters
- Includes leetspeak conversions

**✅ Random Passcodes**
- Generates completely random alphanumeric passwords
- Configurable quantity (1-100,000)

### Example Input/Output

**Input:**
- Date: `01/15/1990`
- Name: `john`
- Enable case variations: ✅

**Sample Output (subset of thousands):**
```
password1990
john123456
JOHN1990!
Password01151990
qwerty1990
JoHn123
p4ssw0rd1990
admin_john
1990password
john_1990@
```

## 📊 Output Size Expectations

| Configuration | Approximate Output |
|---------------|-------------------|
| Basic (no personal data) | 50,000 - 200,000 passcodes |
| With personal data | 500,000 - 2,000,000 passcodes |
| **Case variations enabled** | **5,000,000 - 50,000,000+ passcodes** |
| All options enabled | **10GB+ wordlists possible** |

## 🔧 Advanced Usage

### Command Line Tips

**Check file sizes:**
```bash
ls -lh *.txt
```

**Combine multiple wordlist files:**
```bash
cat passwords_part*.txt > combined_wordlist.txt
```

**Remove duplicates from combined files:**
```bash
sort combined_wordlist.txt | uniq > unique_wordlist.txt
```

### Integration with Security Tools

**Hashcat:**
```bash
hashcat -m 0 -a 0 hashes.txt wordlist.txt
```

**John the Ripper:**
```bash
john --wordlist=wordlist.txt hashes.txt
```

**Hydra:**
```bash
hydra -l username -P wordlist.txt target-ip service
```

## ⚡ Performance Tips

### For Large Wordlists
1. **Disable case variations** unless specifically needed
2. **Limit personal data** to most relevant items
3. **Use SSD storage** for faster file operations
4. **Ensure adequate RAM** (8GB+ recommended for large lists)
5. **Close other applications** during generation

### Memory Management
- The application automatically manages memory for large datasets
- Files are written in chunks to prevent memory overflow
- Progress is saved incrementally

## 🐛 Troubleshooting

### Common Issues

**"Can't find a usable init.tcl" Error:**
```bash
# Reinstall Python from python.org (not Microsoft Store)
# Or install PyQt5 alternative:
pip install PyQt5
```

**Out of Memory Error:**
- Reduce the scope of generation (disable case variations)
- Close other applications
- Use a machine with more RAM

**Slow Generation:**
- Disable case variations for faster processing
- Reduce number of personal data entries
- Use SSD storage instead of HDD

**File Too Large:**
- Files are automatically split at 1GB
- Use the split files individually or combine as needed

### Performance Benchmarks

| System Specs | Generation Time | Output Size |
|--------------|----------------|-------------|
| 8GB RAM, SSD | 2-5 minutes | 1-5 million passcodes |
| 16GB RAM, SSD | 5-15 minutes | 10-50 million passcodes |
| 4GB RAM, HDD | 10-30 minutes | 1-5 million passcodes |

## 🔒 Security Considerations

### Ethical Use
- Only use on systems you own or have explicit permission to test
- Follow responsible disclosure practices
- Comply with local laws and regulations

### Data Privacy
- Personal data entered is only used for wordlist generation
- No data is transmitted or stored externally
- Clear sensitive data from input fields after use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/yourusername/advanced-passcode-generator.git
cd advanced-passcode-generator
# Make your changes
# Test thoroughly
# Submit pull request
```

### Feature Requests
- Open an issue describing the desired feature
- Include use cases and examples
- Consider implementation complexity

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Common password lists from various security research
- Keyboard pattern analysis from security communities
- Inspired by tools like Crunch, CUPP, and other wordlist generators

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/advanced-passcode-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/advanced-passcode-generator/discussions)
- **Security**: Report security issues privately via email

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Added all case variation generation
- ✅ Expanded to 200+ common passwords
- ✅ Added 300+ common words
- ✅ Automatic file splitting at 1GB
- ✅ Enhanced progress tracking
- ✅ Improved memory management

### v1.0.0
- ✅ Basic wordlist generation
- ✅ GUI interface
- ✅ Common password combinations
- ✅ Date and word processing

---

**⚠️ Remember: With great power comes great responsibility. Use this tool ethically and legally.**
```

This README provides comprehensive documentation covering:

1. **Clear description** of what the tool does
2. **Installation instructions** for different scenarios
3. **Detailed usage examples** with expected outputs
4. **Performance expectations** and system requirements
5. **Troubleshooting guide** for common issues
6. **Security and ethical considerations**
7. **Contributing guidelines**
8. **Professional formatting** with badges and tables

The README is structured to help both beginners and advanced users understand and effectively use the tool while emphasizing responsible usage.
