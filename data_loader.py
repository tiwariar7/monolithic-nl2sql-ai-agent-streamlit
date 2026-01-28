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
    def load_sqlite(self, file_path: str) -> Tuple[List[str], bool, str]:
        try:
            self.conn.execute(f"ATTACH '{file_path}' AS sqlite_db (TYPE SQLITE)")
            tables_result = self.conn.execute(
                "SELECT name FROM sqlite_db.sqlite_master WHERE type='table'"
            ).fetchall()            
            if not tables_result:
                return [], False, "No tables found in SQLite database"            
            loaded_tables = []
            for (table_name,) in tables_result:
                if table_name.startswith('sqlite_'):
                    continue
                self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM sqlite_db.{table_name}")
                loaded_tables.append(table_name)
                self.loaded_tables.append(table_name)            
            self.conn.execute("DETACH sqlite_db")            
            if not loaded_tables:
                return [], False, "No user tables found in SQLite database"            
            return loaded_tables, True, f"Successfully loaded {len(loaded_tables)} tables: {', '.join(loaded_tables)}"            
        except Exception as e:
            return [], False, f"Error loading SQLite: {str(e)}"   
