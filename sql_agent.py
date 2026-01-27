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
    def generate_sql(self, question: str, schema: str) -> str:
        try:
            user_prompt = f"""Database Schema:
{schema}
User Question: {question}
Generate SQL query:"""            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                max_tokens=500,
            )            
            sql = response.choices[0].message.content.strip()
            sql = self._clean_sql_response(sql)            
            return sql            
        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")    
    def _clean_sql_response(self, response: str) -> str:
        if response.startswith("```sql"):
            response = response[6:]
        elif response.startswith("```"):
            response = response[3:]        
        if response.endswith("```"):
            response = response[:-3]        
        response = response.strip()       
        lines = response.split('\n')
        sql_lines = [line for line in lines if line.strip() and not line.strip().startswith('--')]        
        return ' '.join(sql_lines)
