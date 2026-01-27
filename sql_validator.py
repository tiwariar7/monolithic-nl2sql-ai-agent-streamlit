import re
from typing import Tuple


class SQLValidator:
    DANGEROUS_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE',
        'TRUNCATE', 'REPLACE', 'RENAME', 'GRANT', 'REVOKE',
        'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'EXEC', 'EXECUTE',
        'ATTACH', 'DETACH', 'PRAGMA'
    ]
    
    def __init__(self):
        pass
    
    def validate(self, sql: str) -> Tuple[bool, str]:
        if not sql or not sql.strip():
            return False, "SQL query is empty"
        
        sql = sql.strip()
        
        if self._contains_multiple_statements(sql):
            return False, "Multiple SQL statements detected. Only single SELECT queries are allowed."
        
        if not self._starts_with_select(sql):
            return False, "Only SELECT queries are allowed. Query must start with SELECT."
        
        dangerous_found = self._contains_dangerous_keywords(sql)
        if dangerous_found:
            return False, f"Dangerous SQL keyword detected: {dangerous_found}. Only SELECT queries are allowed."
        
        injection_detected, injection_msg = self._detect_sql_injection(sql)
        if injection_detected:
            return False, f"Potential SQL injection detected: {injection_msg}"
        
        return True, ""

    def _contains_multiple_statements(self, sql: str) -> bool:
        sql_no_strings = re.sub(r"'[^']*'", '', sql)
        sql_no_strings = re.sub(r'"[^"]*"', '', sql_no_strings)
        sql_no_strings = sql_no_strings.rstrip(';').strip()
        return ';' in sql_no_strings

    def _starts_with_select(self, sql: str) -> bool:
        sql_upper = sql.upper().strip()
        return sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')
    
        
