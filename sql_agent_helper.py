import re
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class SchemaInfo:
    tables: Dict[str, List[str]] = field(default_factory=dict)
class SchemaParser:
    def parse_string(self, schema_str: str) -> SchemaInfo:
        schema_info = SchemaInfo()
        current_table = None        
        lines = schema_str.strip().split('\n')
        for line in lines:
            line = line.strip()            
            if line.startswith('Table:'):
                current_table = line.split('Table:')[1].strip()
                schema_info.tables[current_table] = []
            elif line.startswith('-') or line.startswith('*') or line.startswith('•'):
                if current_table:
                    col_match = re.match(r'[-\*•\s]*([\w]+)', line)
                    if col_match:
                        col_name = col_match.group(1)
                        schema_info.tables[current_table].append(col_name)        
        return schema_info
