import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.dbf_enc_reader.connection import DBFConnection

def test_simple_filter():
    # Load DLL
    dll_path = r"C:\Program Files (x86)\Advantage 10.10\ado.net\1.0\Advantage.Data.Provider.dll"
    DBFConnection.set_dll_path(dll_path)
    
    # Connect to DBF
    source_path = r"C:\Users\campo\Documents\projects\DBF_encrypted\pospcp"
    conn = DBFConnection(source_path, "X3WGTXG5QJZ6K9ZC4VO2")
    conn.connect()
    
    try:
        from System.Data import CommandType
        from Advantage.Data.Provider import AdsCommand
        
        cmd = conn.conn.CreateCommand()
        cmd.CommandType = CommandType.TableDirect
        cmd.CommandText = "VENTA"
        
        # Make sure we're using AOF
        cmd.AdsOptimizedFilters = True
        
        # Get table reader
        reader = cmd.ExecuteExtendedReader()
        
        # Try to find records matching the date
        filter_value = "04/05/2025"
        print(f"\nSearching for F_EMISION = {filter_value}")
        
        # Set AOF filter expression
        filter_expr = f"F_EMISION = '{filter_value}'"
        print(f"Setting AOF filter: {filter_expr}")
        reader.Filter = filter_expr
        
        # Print matching records
        count = 0
        while reader.Read():
            if count < 10:  # Show max 5 records
                print("\nRecord:")
                for i in range(reader.FieldCount):
                    field = reader.GetName(i)
                    value = reader.GetValue(i)
                    print(f"{field}: {value}")
            count += 1
            
        print(f"\nTotal records found: {count}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_simple_filter()
