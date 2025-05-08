import json
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.dbf_enc_reader.core import DBFReader
from src.dbf_enc_reader.connection import DBFConnection

def main():
    # Set the DLL path first
    dll_path = r"C:\\Program Files (x86)\\Advantage 10.10\\ado.net\\1.0\\Advantage.Data.Provider.dll"
    DBFConnection.set_dll_path(dll_path)

    # Initialize reader
    enc_pass = "my pass"
    source_path = r"C:\\Users\\campo\\Documents\\projects\\DBF_encrypted\pospcp"
    table_name = "CANOTA"
    limit_rows = 2
    
    print(f"Connecting to DBF at: {source_path}")
    reader = DBFReader(source_path, enc_pass)

    resullt = reader.to_json(table_name, limit_rows)

    print(resullt)

if __name__ == "__main__":
    main()