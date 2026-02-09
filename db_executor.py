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
