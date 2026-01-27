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
