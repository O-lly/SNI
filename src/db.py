#src/db.py
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, Index
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

os.makedirs("post_history", exist_ok=True)

Base = declarative_base()

class PostHistory(Base):
    __tablename__ = "post_history"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    retries = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_source_processed", "source", "processed")
    )

    # URL usa o driver duckdb-engine
    DATABASE_URL = "duckdb:///post_history/posts.duckdb"

    engine = create_engine(DATABASE_URL, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def init_db():
        """Cria o arquivo .duckdb e as tabelas se não existirem."""
        Base.metadata.create_all(bind=engine)