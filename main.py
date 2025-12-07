from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="TPE SNS API")

# メモリ上のデータベース（起動中だけ保持）
posts_db = []
post_counter = 1


# ---------- Pydantic モデル ----------
class PostCreateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=20)
    content: str = Field(..., min_length=1, max_length=1000)
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    tags: Optional[List[str]] = Field(default=None)


class PostCreateResponse(BaseModel):
    post_id: int
    message: str


class PostSummary(BaseModel):
    post_id: int
    user_id: int
    user_name: str = "User"  # 本来はDBから取得
    title: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: datetime


class PostDetailResponse(BaseModel):
    post_id: int
    user_id: int
    title: Optional[str]
    content: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: datetime


# ---------- 共通：ヘッダ X-User-ID 取得 ----------
def get_current_user_id(x_user_id: int = Header(...)):
    """
    リクエストヘッダ "X-User-ID" から user_id を取得する関数
    """
    return x_user_id


# ---------- API 実装 ----------

# 1. 新規投稿
@app.post("/posts", response_model=PostCreateResponse)
def create_post(request: PostCreateRequest, x_user_id: int = Header(...)):

    global post_counter

    new_post = {
        "post_id": post_counter,
        "user_id": x_user_id,
        "title": request.title,
        "content": request.content,
        "start_at": request.start_at,
        "end_at": request.end_at,
        "tags": request.tags or [],
        "created_at": datetime.now()
    }

    posts_db.append(new_post)
    post_counter += 1

    return PostCreateResponse(
        post_id=new_post["post_id"],
        message="投稿を作成しました"
    )


# 2. 投稿一覧取得
@app.get("/posts", response_model=List[PostSummary])
def list_posts():

    result = []
    for post in posts_db:
        result.append(PostSummary(
            post_id=post["post_id"],
            user_id=post["user_id"],
            title=post["title"],
            start_at=post["start_at"],
            end_at=post["end_at"],
            created_at=post["created_at"],
        ))

    return result


# 3. 投稿詳細取得
@app.get("/posts/{post_id}", response_model=PostDetailResponse)
def get_post_detail(post_id: int):

    for post in posts_db:
        if post["post_id"] == post_id:
            return PostDetailResponse(**post)

    raise HT
