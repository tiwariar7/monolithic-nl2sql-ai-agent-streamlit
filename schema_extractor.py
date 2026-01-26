import duckdb

class SchemaExtractor:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn    
