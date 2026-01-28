import duckdb
import pandas as pd
import os

class DataLoader:  
    def __init__(self, db_path: str = ":memory:"):
        self.conn = duckdb.connect(db_path)
        self.loaded_tables: List[str] = [] 
