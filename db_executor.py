import duckdb

lass DBExecutor:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn
