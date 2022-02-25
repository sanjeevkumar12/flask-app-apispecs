from dataclasses import dataclass
from typing import List, Optional


@dataclass
class APIUser:
    first_name: str
    email: str
    last_name: str
    password: str
    id: Optional[int] = None
    password_hash: Optional[str] = ""
