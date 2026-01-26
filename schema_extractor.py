import duckdb
from typing import Dict, List, Optional
class SchemaExtractor:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn    
    def get_schema(self) -> Dict[str, List[Dict[str, str]]]:
        try:
            schema = {}
            tables_result = self.conn.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            ).fetchall()            
            for (table_name,) in tables_result:
                columns = self.get_table_columns(table_name)
                if columns:
                    schema[table_name] = columns            
            return schema            
        except Exception as e:
            print(f"Error extracting schema: {str(e)}")
            return {}    
    def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        try:
            columns_result = self.conn.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                AND table_schema = 'main'
                ORDER BY ordinal_position
            """).fetchall()            
            columns = [
                {'name': col_name, 'type': data_type}
                for col_name, data_type in columns_result
            ]            
            return columns            
        except Exception as e:
            print(f"Error getting columns for table {table_name}: {str(e)}")
            return []
