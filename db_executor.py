import duckdb

class DBExecutor:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn
