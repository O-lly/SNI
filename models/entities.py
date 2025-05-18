# models/entities.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    id: str
    author: str
    content: str
    media_gallery: list[str]
    timestamp: datetime
    source: str