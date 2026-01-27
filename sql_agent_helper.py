import re
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class SchemaInfo:
    tables: Dict[str, List[str]] = field(default_factory=dict)
