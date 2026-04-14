from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from app.models.gameSessionUserLink import GameSessionUserLink
from app.models.gameNightUserLink import GameNightUserLink

if TYPE_CHECKING:
    from app.models.gameSession import GameSession
    from app.models.gameNight import GameNight

class UserBoardGameBase(SQLModel):
    username: str = Field(index=True, max_length=50, sa_column_kwargs={"unique": True})
    email: str = Field(index=True, max_length=254)
    profile_image_url: str | None = None

class UserBoardGame(UserBoardGameBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str = Field(default="")
    apple_id: str | None = Field(default=None, sa_column_kwargs={"unique": True, "nullable": True}, index=True)
    won_sessions: list["GameSession"] = Relationship(back_populates="winners", link_model=GameSessionUserLink)
    game_nights: list["GameNight"] = Relationship(link_model=GameNightUserLink, back_populates="users")

class UserBoardGamePublic(SQLModel):
    id: int
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    profile_image_url: str | None = None

class UserBoardGameCreate(UserBoardGameBase):
    password: str = Field(min_length=8, max_length=128)

class UserBoardGameUpdate(SQLModel):
    username: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=254)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    profile_image_url: str | None = None

class UserBoardGameClientFacing(SQLModel):
    id: int
    username: str

