# services/formatters/reddit_formatter.py

from models.interfaces import ContentFormatter
from models.entities import Post
from datetime import datetime

class RedditFormatter(ContentFormatter):
    source_name = "reddit"

    def format(self, raw: dict) -> Post:
        return Post(
            id=raw["id"],
            author=raw["author"],
            content=raw["content"],
            media_gallery=raw.get("media_gallery", []),
            timestamp=datetime.utcfromtimestamp(raw["timestamp"]),
            source=self.source_name
        )