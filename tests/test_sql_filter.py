import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.dbf_enc_reader.core import DBFReader
from src.dbf_enc_reader.connection import DBFConnection

def test_sql_filtering():
    # Set the DLL path first
    dll_path = r"C:\\Program Files (x86)\\Advantage 10.10\\ado.net\\1.0\\Advantage.Data.Provider.dll"
    print(f"\nChecking if DLL exists at: {dll_path}")
    if not os.path.exists(dll_path):
        print("Error: DLL not found!")
        return
        
    print("DLL found, loading...")
    DBFConnection.set_dll_path(dll_path)
    print("DLL loaded successfully")

    # Initialize connection
    enc_pass = "X3WGTXG5QJZ6K9ZC4VO2"
    source_path = str(Path(r"C:\Users\campo\Documents\projects\DBF_encrypted\pospcp").resolve())
    table_name = "VENTA"
    
    print(f"\nConnecting to DBF at: {source_path}")
    conn = DBFConnection(source_path, enc_pass)
    
    # Test different SQL WHERE clauses
    test_cases = [
        "SELECT * FROM VENTA WHERE F_EMISION = '05/05/2025'",
        "SELECT * FROM VENTA WHERE F_EMISION >= '05/05/2025' AND F_EMISION < '05/06/2025'",
        "SELECT * FROM VENTA WHERE SUBSTRING(F_EMISION, 1, 2) = '05' AND SUBSTRING(F_EMISION, 4, 2) = '05' AND SUBSTRING(F_EMISION, 7, 4) = '2025'",
        "SELECT * FROM VENTA WHERE F_EMISION BETWEEN '05/05/2025' AND '05/05/2025'"
    ]
    
    for sql_query in test_cases:
        print(f"\n\nTesting SQL query: {sql_query}")
        try:
            reader = conn.get_reader(table_name, sql_query)
            results = []
            while reader.Read():
                record = {}
                for i in range(reader.FieldCount):
                    field_name = reader.GetName(i)
                    value = reader.GetValue(i)
                    record[field_name] = value
                results.append(record)
                
            print(f"Success! Found {len(results)} records")
            if results:
                print("First record:")
                print(json.dumps(results[0], indent=4))
        except Exception as e:
            print(f"Error: {str(e)}")
            
    conn.close()

if __name__ == "__main__":
    test_sql_filtering()
