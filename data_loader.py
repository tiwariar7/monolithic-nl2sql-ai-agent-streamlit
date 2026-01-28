import duckdb
import pandas as pd
import os
from typing import Optional, List, Tuple

class DataLoader:  
    def __init__(self, db_path: str = ":memory:"):
        self.conn = duckdb.connect(db_path)
        self.loaded_tables: List[str] = []    
    def load_csv(self, file_path: str, table_name: Optional[str] = None) -> Tuple[str, bool, str]:
        try:
            if table_name is None:
                table_name = self._generate_table_name(file_path)
            df = pd.read_csv(file_path)            
            if df.empty:
                return table_name, False, "CSV file is empty"
            df.columns = [self._clean_column_name(col) for col in df.columns]            
            self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            self.loaded_tables.append(table_name)            
            return table_name, True, f"Successfully loaded {len(df)} rows into table '{table_name}'"
        except Exception as e:
            return table_name or "unknown", False, f"Error loading CSV: {str(e)}"

    def load_excel(self, file_path: str, table_name: Optional[str] = None, sheet_name: int = 0) -> Tuple[str, bool, str]:
        try:
            if table_name is None:
                table_name = self._generate_table_name(file_path)            
            df = pd.read_excel(file_path, sheet_name=sheet_name)            
            if df.empty:
                return table_name, False, "Excel file is empty"            
            df.columns = [self._clean_column_name(col) for col in df.columns]            
            self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            self.loaded_tables.append(table_name)            
            return table_name, True, f"Successfully loaded {len(df)} rows into table '{table_name}'"            
        except Exception as e:
            return table_name or "unknown", False, f"Error loading Excel: {str(e)}" 
