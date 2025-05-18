# services/publishers/email_publisher.py

from models.interfaces import ContentPublisher
from services.post_history_repository import PostHistoryRepository

class EmailPublisher(ContentPublisher):
    target_name = "email"

    def __init__(self, mailer, repository: PostHistoryRepository, receiver: str):
        self.mailer = mailer
        self.repository = repository
        self.receiver = receiver
    
    async def publish(self, post):
        subject = f"Novo post de {post.source}: {post.id}"
        body = post.content
        self.mailer.send_email(
            receiver=self.receiver,
            subject=subject,
            content=body,
            attachs=post.media_gallery
        )
        self.repository.mark_processed(post.id, self.target_name)