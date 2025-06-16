# Advanced Passcode Generator

A comprehensive GUI-based tool for generating custom wordlists and passcode dictionaries for security testing, password recovery, and penetration testing purposes.

## 🚀 Features

### **Core Generation Methods**
- **📅 Date-based Passcodes**: Generate variations from important dates (birthdays, anniversaries, etc.)
- **📝 Word-based Passcodes**: Create combinations from names, places, and personal words
- **🎲 Random Passcodes**: Generate truly random alphanumeric combinations
- **🔑 Common Passwords**: Include 200+ most common passwords and patterns
- **🧠 Smart Combinations**: Intelligently combine user data with common passwords

### **Advanced Features**
- **🔄 Case Variations**: Generate ALL possible upper/lowercase combinations (e.g., "hello" → "HeLLo", "hELLO", etc.)
- **📏 Length Filtering**: Set minimum and maximum password lengths
- **🔗 Pattern Recognition**: Automatic keyboard patterns, number sequences, and year variations
- **💬 Leetspeak**: Automatic conversion to leetspeak (e.g., "hello" → "h3ll0")
- **📊 Duplicate Removal**: Automatically removes duplicate entries

### **Output Customization**
- **📋 Multiple Delimiters**: Choose from various output formats:
  - New Line (```\n```) - Default text format
  - Comma (```,```) - CSV format
  - Semicolon (```;```) - Alternative CSV format
  - Tab (```\t```) - TSV format
  - Space - Space-separated values
  - Pipe (```|```) - Pipe-separated values
  - Custom - Define your own delimiter (supports escape sequences)
- **📁 Smart File Extensions**: Automatic file extension selection (.txt, .csv, .tsv)
- **✂️ File Splitting**: Automatically splits large wordlists into 1GB chunks

### **Data Management**
- **📂 External Data Files**: Common passwords, patterns, and words stored in separate text files
- **🔄 Fallback System**: Works even if data files are missing
- **📊 File Status Display**: Shows which data files are loaded and entry counts
- **💾 Progress Tracking**: Real-time progress updates during generation

## 📋 Requirements

- Python 3.6+
- tkinter (usually included with Python)
- No additional dependencies required!

## 🛠️ Installation

1. **Download the files:**
   ```bash
   git clone [repository-url]
   cd passcode-generator
   ```

2. **Set up data files** (choose one option):

   **Option A: Same Directory**
   ```
   passcode_generator.py
   common_passwords.txt
   common_patterns.txt
   common_words.txt
   ```

   **Option B: Data Subdirectory**
   ```
   passcode_generator.py
   data/
     ├── common_passwords.txt
     ├── common_patterns.txt
     └── common_words.txt
   ```

3. **Run the application:**
   ```bash
   python passcode_generator.py
   ```

## 📁 Data Files

### **common_passwords.txt**
Contains 200+ most common passwords including:
- Top leaked passwords (password, 123456, qwerty, etc.)
- Common patterns and variations
- Popular culture references
- Default passwords

### **common_patterns.txt**
Contains common patterns such as:
- Number sequences (123, 321, 1234, etc.)
- Years (2024, 2023, 1990, etc.)
- Keyboard patterns (qwerty, asdf, zxc, etc.)
- Short number combinations

### **common_words.txt**
Contains 300+ common words including:
- Emotions and relationships
- Colors and animals
- Nature and food
- Technology terms
- Sports and games
- Places and locations

### **File Format**
- One entry per line
- Comments supported (lines starting with ```#```)
- UTF-8 encoding
- Empty lines automatically ignored

## 🎯 Usage Guide

### **Basic Usage**
1. **Launch the application**
2. **Configure length settings** (min/max password length)
3. **Choose output format** (delimiter type)
4. **Select generation methods:**
   - Check desired generation types
   - Enter personal data (dates, words)
   - Configure case variations (⚠️ Warning: can generate millions of combinations)
5. **Click "Generate Passcodes"**
6. **Choose save location**

### **Input Examples**

**Dates:**
```
01/15/1990
12-25-2000
2023
June 15, 1985
```

**Words/Names:**
```
john
smith
fluffy
company123
MyPet
```

### **Output Examples**

**New Line Format (.txt):**
```
password123
john1990
FLUFFY!
Smith2023
```

**CSV Format (.csv):**
```
password123,john1990,FLUFFY!,Smith2023
```

**Custom Delimiter:**
```
password123|john1990|FLUFFY!|Smith2023
```

## ⚙️ Configuration Options

### **Length Settings**
- **Minimum Length**: 1-50 characters
- **Maximum Length**: 1-50 characters
- Filters all generated passwords to specified range

### **Case Variations**
- **Basic**: original, lowercase, UPPERCASE, Capitalized
- **ALL Combinations**: Every possible upper/lower combination
  - ⚠️ **Warning**: Can generate millions of passwords!
  - Example: "hello" → hello, Hello, hEllo, heLlo, helLo, hellO, HEllo, etc.

### **Output Delimiters**
| Option | Character | File Extension | Use Case |
|--------|-----------|----------------|----------|
| New Line | ```\n``` | .txt | Standard wordlists |
| Comma | ```,``` | .csv | Spreadsheet import |
| Semicolon | ```;``` | .csv | European CSV format |
| Tab | ```\t``` | .tsv | Tab-separated data |
| Space | ``` ``` | .txt | Space-separated lists |
| Pipe | ```\|``` | .txt | Database imports |
| Custom | User-defined | .txt | Special formats |

### **Smart Combinations**
Automatically creates intelligent combinations:
- **Common + User Words**: password + john → passwordjohn, johnpassword
- **Common + Dates**: admin + 1990 → admin1990, 1990admin
- **Words + Dates**: john + 1990 → john1990, 1990john
- **With Special Characters**: john1990!, admin@2023, etc.

## 📊 Performance & File Management

### **File Splitting**
- Automatically splits files larger than 1GB
- Creates numbered parts: ```wordlist_part1.txt```, ```wordlist_part2.txt```
- Maintains chosen delimiter format across all files

### **Memory Management**
- Efficient duplicate removal
- Progress tracking for large generations
- Graceful handling of massive wordlists

### **Expected Output Sizes**
| Configuration | Approximate Output |
|---------------|-------------------|
| Basic (no case variations) | 10K - 100K passwords |
| With case variations | 1M - 10M+ passwords |
| All features enabled | 10M+ passwords, multiple GB |

## ⚠️ Important Warnings

### **Case Variations**
- **ALL case variations** can generate **MASSIVE** wordlists
- A single 5-letter word generates 32 combinations
- Multiple words can create millions of passwords
- Use with caution on slower systems

### **File Sizes**
- Large wordlists are automatically split into 1GB files
- With all features enabled, expect multiple gigabytes of output
- Ensure sufficient disk space before generation

### **Legal Notice**
This tool is intended for:
- ✅ Security testing on systems you own
- ✅ Password recovery for your own accounts
- ✅ Penetration testing with proper authorization
- ✅ Educational and research purposes

**NOT for:**
- ❌ Unauthorized access to systems
- ❌ Illegal activities
- ❌ Attacking systems without permission

## 🐛 Troubleshooting

### **Data Files Not Loading**
- Check file locations (same directory or ```data/``` subdirectory)
- Verify file encoding is UTF-8
- Check file permissions
- App will use fallback data if files are missing

### **Large File Generation Issues**
- Ensure sufficient disk space (multiple GB may be needed)
- Close other applications to free memory
- Consider disabling case variations for initial testing

### **Performance Issues**
- Reduce the number of input words/dates
- Disable case variations
- Generate smaller batches
- Close unnecessary applications

## 🔄 Updates & Customization

### **Adding Custom Data**
1. Edit the ```.txt``` files to add your own:
   - Common passwords
   - Patterns
   - Words
2. Use ```#``` for comments in data files
3. One entry per line

### **Example Custom Data File**
```
# My custom passwords
mycompany123
corporatepass
# Common patterns in my organization
2024corp
admin2024
# Comments are ignored
password2024
```

## 📈 Version History

### **Latest Version Features**
- ✅ External data file support
- ✅ Multiple delimiter options
- ✅ File status display
- ✅ Automatic file extension selection
- ✅ Enhanced case variation system
- ✅ Smart combination algorithms
- ✅ Progress tracking improvements
- ✅ Graceful error handling

## 🤝 Contributing

Feel free to contribute by:
- Adding more common passwords/patterns
- Improving generation algorithms
- Enhancing the user interface
- Reporting bugs and issues
- Suggesting new features

## 📄 License

This project is provided for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

---

**Remember**: Always use this tool responsibly and only on systems you own or have explicit permission to test! 🔒