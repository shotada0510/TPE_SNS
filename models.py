from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.types import JSON
from datetime import datetime
from db import Base


class UserPost(Base):
    __tablename__ = "user_posts"

    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String(20))
    content = Column(Text)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    tags = Column(JSON)   # ← タグを JSON で保存（簡易版）
    created_at = Column(DateTime, default=datetime.utcnow)
