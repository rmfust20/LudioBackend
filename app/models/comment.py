from sqlmodel import Field, Session, SQLModel, create_engine, select

class Comment(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id", index=True)
    content: str = Field(default="", max_length=5000)
    parent_comment_id: int | None = Field(default=None, foreign_key="comment.id", index=True)

class GameNightComment(Comment, table=True):
    game_night_id: int = Field(foreign_key="gamenight.id", index=True)

class ReviewComment(Comment, table=True):
    review_id: int = Field(foreign_key="review.id", index=True)
    

class CommentLike(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", index=True, primary_key=True)
    comment_id: int = Field(foreign_key="comment.id", index=True, primary_key=True)

