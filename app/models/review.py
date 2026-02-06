from sqlmodel import Field, Session, SQLModel, create_engine, select


class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    board_game_id: int = Field(foreign_key="boardgame.id", index=True)
    user_id: int = Field(foreign_key="userboardgame.id", index=True)
    username: str = Field(index=True)
    rating: int | None = Field(default=None)
    comment: str | None = Field(default=None)
    date_created: str | None = Field(default=None)

class ReviewUpdate(SQLModel):
    rating: int | None = Field(default=None)
    comment: str | None = Field(default=None)
    date_created: str | None = Field(default=None)


