from decimal import Decimal
from typing import Any

class DataConverter:
    def smart_trim(self, value: Any) -> Any:
        """
        Trim spaces intelligently based on value type.
        
        Args:
            value: Value to trim
            
        Returns:
            Trimmed value maintaining its type
        """
        if isinstance(value, str):
            return value.rstrip()  # Only right trim for strings
        elif isinstance(value, (int, float, Decimal)):
            return value  # Don't trim numbers
        elif value is None:
            return None
        return value

    def convert_value(self, value: Any) -> Any:
        """
        Convert a value from DBF to Python native type.
        
        Args:
            value: Value to convert
            
        Returns:
            Converted value
        """
        if value is None:
            return None
            
        # Handle .NET types that aren't JSON serializable
        if hasattr(value, 'ToString'):
            value = str(value)
            
        # Apply smart trimming after conversion
        return self.smart_trim(value)
