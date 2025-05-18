# services/post_history_repository.py

from sqlalchemy.exc import IntegrityError
from services.db import SessionLocal, PostHistory

class PostHistoryRepository:
    def __init__(self):
        self.session = SessionLocal()
    
    def mark_processed(self, post_id: str, source: str):
        try:
            ph = PostHistory(id=post_id, source=source, processed=True)
            self.session.add(ph)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            ph = self.session.get(PostHistory, post_id)
            if ph:
                ph.processed = True
                self.session.commit()
    
    def is_processed(self, post_id: str) -> bool:
        ph = self.session.get(PostHistory, post_id)
        return bool(ph and ph.processed)