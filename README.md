# DBF Encrypted Reader

A Python library for reading and processing encrypted DBF files.

## Project Structure
```
DBF_encrypted/
├── src/
│   ├── dbf_reader/
│   │   ├── __init__.py
│   │   ├── core.py          # Core DBF reading functionality
│   │   ├── crypto.py        # Encryption/decryption handling
│   │   └── exceptions.py    # Custom exceptions
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py       # Helper functions
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py         # Core functionality tests
│   ├── test_crypto.py       # Encryption tests
│   └── fixtures/            # Test DBF files
├── examples/
│   ├── basic_usage.py       # Basic usage examples
│   └── advanced_usage.py    # Advanced usage examples
├── docs/
│   ├── installation.md      # Installation guide
│   └── api.md              # API documentation
├── requirements.txt         # Project dependencies
├── setup.py                # Package setup file
├── LICENSE                 # License file
└── README.md              # This file

## Features
- Read encrypted and unencrypted DBF files
- Support for various DBF formats
- PYODBC integration
- Easy-to-use API
- Comprehensive error handling

## Installation
```bash
pip install -r requirements.txt
```

## Usage Example
```python
from dbf_reader import DBFReader

# Initialize reader
reader = DBFReader('path/to/file.dbf')

# Read encrypted DBF
data = reader.read_encrypted(encryption_key='your-key')

# Convert to dictionary/JSON format
json_data = data.to_json()
```

## Development Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run tests

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License