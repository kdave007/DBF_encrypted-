import clr
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from .connection import DBFConnection
from .converters import DataConverter

class DBFReader:
    def __init__(self, data_source: str, encryption_password: str):
        """
        Initialize DBF reader with connection parameters.
        
        Args:
            data_source: Path to the DBF file
            encryption_password: Password for encrypted DBF
        """
        self.connection = DBFConnection(data_source, encryption_password)
        self.converter = DataConverter()

    def read_table(self, table_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Read records from specified table.
        
        Args:
            table_name: Name of the table to read
            limit: Optional limit on number of records to read
            
        Returns:
            List of dictionaries containing the records
        """
        with self.connection as conn:
            reader = conn.get_reader(table_name)
            field_count = reader.FieldCount
            columns = [reader.GetName(i) for i in range(field_count)]
            
            results = []
            record_count = 0
            
            while reader.Read():
                if limit and record_count >= limit:
                    break
                    
                row_dict = {}
                for col in columns:
                    try:
                        value = reader[col]
                        row_dict[col] = self.converter.convert_value(value)
                    except Exception as e:
                        row_dict[col] = f"Error reading {col}: {str(e)}"
                
                results.append(row_dict)
                record_count += 1
            
            return results

    def to_json(self, table_name: str, limit: Optional[int] = None) -> str:
        """
        Convert table records to JSON string.
        
        Args:
            table_name: Name of the table to convert
            limit: Optional limit on number of records to convert
            
        Returns:
            JSON string representation of the records
        """
        records = self.read_table(table_name, limit)
        return json.dumps(records, indent=4, ensure_ascii=False)

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about table structure.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table metadata
        """
        with self.connection as conn:
            reader = conn.get_reader(table_name)
            return {
                'field_count': reader.FieldCount,
                'columns': [reader.GetName(i) for i in range(reader.FieldCount)]
            }
