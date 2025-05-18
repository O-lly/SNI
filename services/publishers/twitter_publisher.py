# services/publishers/twitter_publisher.py

from models.interfaces import ContentPublisher
from services.post_history_repository import PostHistoryRepository

class TwitterPublisher(ContentPublisher):
    target_name = "twitter"

    def __init__(self, client, repository: PostHistoryRepository):
        self.client = client
        self.repository = repository

    async def publish(self, post):
        await self.client.send_post(content=post.content, media_gallery=post.media_gallery)
        self.repository.mark_processed(post.id, self.target_name)