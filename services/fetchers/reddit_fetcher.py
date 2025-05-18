# services/fetchers/reddit_fetcher.py

from models.interfaces import ContentFetcher
from services.post_history_repository import PostHistoryRepository
import praw

class RedditFetcher(ContentFetcher):
    source_name = "reddit"

    def __init__(self, credentials: dict, repository: PostHistoryRepository, subreddit: str, filter: str, limit: int):
        self.repository = repository
        self.limit = limit
        self.filter = filter
        self.reddit = praw.Reddit(**credentials)
        self.subreddit = self.reddit.subreddit(subreddit)

    async def fetch(self) -> list[dict]:
        raws = []
        if self.filter == "new":
            posts = self.subreddit.new(limit=self.limit)
        else:
            posts = self.subreddit.hot(limit=self.limit)
        
        for post in posts:
            if not self.repository.is_processed(post.id):
                raws.append({
                    "id": post.id,
                    "author": post.author.name,
                    "content": post.title,
                    "media_gallery": [],
                    "timestamp": post.created_utc
                })
                self.repository.mark_processed(post.id, self.source_name)
        return raws