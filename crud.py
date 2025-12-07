from sqlalchemy.orm import Session
from models import UserPost
from datetime import datetime


def create_post(db: Session, user_id: int, body):
    post = UserPost(
        user_id=user_id,
        title=body.title,
        content=body.content,
        start_at=body.start_at,
        end_at=body.end_at,
        tags=body.tags,
        created_at=datetime.utcnow(),
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int):
    return db.query(UserPost).filter(UserPost.post_id == post_id).first()


def update_post(db: Session, post_id: int, body):
    post = get_post(db, post_id)
    if not post:
        return None

    post.title = body.title
    post.content = body.content
    post.start_at = body.start_at
    post.end_at = body.end_at
    post.tags = body.tags

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)
    if not post:
        return None
    db.delete(post)
    db.commit()
    return True


def list_posts(db: Session, q: str, page: int):
    query = db.query(UserPost)

    if q:
        query = query.filter(
            (UserPost.content.contains(q)) |
            (UserPost.title.contains(q))
        )

    total = query.count()
    limit = 20
    offset = (page - 1) * limit

    posts = query.order_by(UserPost.start_at.asc()).offset(offset).limit(limit).all()

    return posts, total
