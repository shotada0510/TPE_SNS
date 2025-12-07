from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PostCreateRequest(BaseModel):
    title: Optional[str]
    content: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    tags: Optional[List[str]]


class PostCreateResponse(BaseModel):
    post_id: int
    message: str


class PostSummary(BaseModel):
    post_id: int
    user_id: int
    title: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: datetime


class PostListResponse(BaseModel):
    page: int
    limit: int
    total: int
    posts: List[PostSummary]


class PostDetailResponse(BaseModel):
    post_id: int
    user_id: int
    title: Optional[str]
    content: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: datetime
