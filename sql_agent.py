import os
import re
from typing import Optional, List, Tuple

class SQLAgent:
    SYSTEM_PROMPT = """You are an expert SQL query generator. Convert natural language questions to valid SQL SELECT queries.
CRITICAL RULES:
1. Generate ONLY SELECT queries
2. Use ONLY tables and columns from the provided schema
3. Return ONLY the SQL query - no explanations, no markdown, no extra text
4. If the question cannot be answered with the schema, return: ERROR: Insufficient schema
5. Use proper SQL syntax compatible with SQLite/DuckDB
6. Handle dates, joins, aggregations, and complex queries correctly
RESPONSE FORMAT:
Output ONLY the SQL query as plain text. No markdown code blocks, no explanations."""   
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key required. Set GROQ_API_KEY environment variable or pass api_key parameter.")        
        self.model = model        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError("Groq package required. Install with: pip install groq")    
  
