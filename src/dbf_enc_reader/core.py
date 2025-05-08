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

    def read_table(self, table_name: str, limit: Optional[int] = None, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Read records from a table with optional filters.
        
        Args:
            table_name: Name of the table to read
            limit: Optional limit on number of records to read
            filters: Optional list of filter conditions. Each filter is a dict with:
                - 'field': Field name to filter on
                - 'value': Value to compare against for normal filters
                - 'operator': Comparison operator ('=', '>', '<', '>=', '<=', 'range')
                - 'from_value': Start value for range filters
                - 'to_value': End value for range filters
                - 'is_date': Whether this is a date field
            
        Returns:
            List of records as dictionaries
        """
        results = []
        with self.connection as conn:
            reader = conn.get_reader(table_name)
            
            # Get total records first
            total_records = 0
            while reader.Read():
                total_records += 1
            
            # Reset reader position
            reader.Close()
            reader = conn.get_reader(table_name)
            
            # Read records from newest to oldest
            count = 0
            records_to_skip = 0
            
            while reader.Read():
                # Skip records until we reach the desired starting point
                if records_to_skip < total_records - 1:
                    records_to_skip += 1
                    continue
                    
                if limit and count >= limit:
                    break
                    
                record = {}
                for i in range(reader.FieldCount):
                    field_name = reader.GetName(i)
                    value = reader.GetValue(i)
                    record[field_name] = self.converter.convert_value(value)
                    

                
                # Apply filters in memory
                if filters and not self._apply_filters(record, filters):
                    continue
                    
                results.append(record)
                count += 1
                records_to_skip -= 1
            
            return results
            
    def _apply_filters(self, record: Dict[str, Any], filters: List[Dict[str, Any]]) -> bool:
        """Apply filters to a record in memory.
        
        Args:
            record: The record to filter
            filters: List of filter conditions
            
        Returns:
            True if record matches all filters, False otherwise
        """
        from datetime import datetime
        
        for f in filters:
            field = f['field']
            operator = f.get('operator', '=')
            is_date = f.get('is_date', False)
            
            if field not in record:
                return False
                
            record_value = record[field]
            
            if is_date:
                def parse_date(date_str):
                    # Extract just the date part (assuming dd/mm/yyyy format)
                    date_part = date_str.split(' ')[0]
                    try:
                        result = datetime.strptime(date_part, '%d/%m/%Y')
                        return result
                    except ValueError as e:
                        print(f"Error parsing date: {date_str} -> {str(e)}")
                        raise
                
                # Convert date strings to datetime objects
                if operator == 'range':
                    from_value = parse_date(f['from_value'])
                    to_value = parse_date(f['to_value'])
                    record_date = parse_date(record_value)
                    if not (from_value <= record_date <= to_value):
                        return False
                else:
                    filter_date = parse_date(f['value'])
                    record_date = parse_date(record_value)
                    
                    if operator == '=' and record_date != filter_date:
                        return False
                    elif operator == '>' and record_date <= filter_date:
                        return False
                    elif operator == '<' and record_date >= filter_date:
                        return False
                    elif operator == '>=' and record_date < filter_date:
                        return False
                    elif operator == '<=' and record_date > filter_date:
                        return False
            else:
                # Handle non-date comparisons
                filter_value = f['value']
                
                if operator == '=' and record_value != filter_value:
                    return False
                elif operator == '>' and record_value <= filter_value:
                    return False
                elif operator == '<' and record_value >= filter_value:
                    return False
                elif operator == '>=' and record_value < filter_value:
                    return False
                elif operator == '<=' and record_value > filter_value:
                    return False
                
        return True

    def to_json(self, table_name: str, limit: Optional[int] = None, filters: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Convert table records to JSON string.
        
        Args:
            table_name: Name of the table to convert
            limit: Optional limit on number of records to convert
            filters: Optional list of filter conditions
            
        Returns:
            JSON string representation of the records
        """
        records = self.read_table(table_name, limit, filters)
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
