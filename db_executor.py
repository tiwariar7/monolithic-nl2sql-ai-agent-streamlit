import duckdb
import pandas as pd
from typing import Tuple, Optional


class DBExecutor:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn

    def execute_query(self, sql: str) -> Tuple[bool, Optional[pd.DataFrame], str]:
        try:
            result = self.conn.execute(sql)
            df = result.df()            
            if df.empty:
                return True, df, "Query executed successfully. No rows returned."            
            row_count = len(df)
            col_count = len(df.columns)            
            return True, df, f"Query executed successfully. Returned {row_count} row(s) with {col_count} column(s)."            
        except Exception as e:
            error_msg = self._format_error_message(str(e))

    def _format_error_message(self, error: str) -> str:
        error_lower = error.lower()        
        if 'table' in error_lower and 'does not exist' in error_lower:
            return f"Table not found: {error}\n\nPlease check that the table name matches the schema."        
        elif 'column' in error_lower and ('does not exist' in error_lower or 'not found' in error_lower):
            return f"Column not found: {error}\n\nPlease check that the column name matches the schema."        
        elif 'syntax error' in error_lower:
            return f"SQL syntax error: {error}\n\nThe generated SQL query has invalid syntax."        
        elif 'ambiguous' in error_lower:
            return f"Ambiguous column reference: {error}\n\nPlease specify the table name or use aliases."        
        elif 'conversion' in error_lower or 'cast' in error_lower:
            return f"Data type error: {error}\n\nCannot convert data to the requested type."        
        else:
            return f"Query execution error: {error}"
