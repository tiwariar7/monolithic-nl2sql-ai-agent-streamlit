import duckdb

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
