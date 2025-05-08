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
└── README.md              # DBF Encrypted Reader

## Prerequisites

1. Python 3.x
2. Advantage Data Provider installed (version 10.10 or later)
3. Required Python packages (install via `pip install -r requirements.txt`)

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Ensure Advantage Data Provider is properly installed
2. Locate your Advantage.Data.Provider.dll path (typically in Program Files)
3. Configure the DLL path in your code

## Usage Example

```python
from src.dbf_enc_reader.core import DBFReader
from src.dbf_enc_reader.connection import DBFConnection

def main():
    # Set the DLL path first
    dll_path = "path/to/Advantage.Data.Provider.dll"
    DBFConnection.set_dll_path(dll_path)

    # Initialize reader with your DBF path and encryption password
    reader = DBFReader("path/to/dbf/folder", "your_encryption_password")

    # Read records from a table (optional limit)
    result = reader.to_json("TABLE_NAME", limit=2)
    print(result)
```

## Features

- Read encrypted DBF files securely
- Convert DBF records to JSON format
- Limit number of records returned
- Proper connection management and cleanup
- Error handling for common issues

## Security Notes

- Never store encryption passwords in code
- Use environment variables or secure configuration management
- Keep DLL paths in configuration files

## Testing

To run the test class:
```bash
python tests/test_class.py
```

Make sure to:
1. Update the DLL path
2. Set proper encryption password
3. Configure correct DBF file path
4. Specify the table name you want to read

## Error Handling

The library includes error handling for common issues:
- Missing DLL
- Invalid paths
- Connection problems
- Encryption errors

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

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