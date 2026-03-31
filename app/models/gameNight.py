from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from app.models.gameNightUserLink import GameNightUserLink
from app.models.user import UserBoardGamePublic
from app.models.boardGame import BoardGame

if TYPE_CHECKING:
    # This only runs during static analysis (IDE/Mypy), not at runtime
    from app.models.gameSession import GameSession
    from app.models.user import UserBoardGame

class GameNight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    host_user_id: int = Field(foreign_key="userboardgame.id", index=True)

    game_night_date: date | None = Field(default=None)
    description: Optional[str] = Field(default=None)

    # IMPORTANT: default_factory=list
    sessions: list["GameSession"] = Relationship(back_populates="game_night")

    images: list["GameNightImage"] = Relationship(back_populates="game_night")
    users: list["UserBoardGame"] = Relationship(link_model=GameNightUserLink, back_populates="game_nights")

class GameNightImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    image_url: Optional[str] = None

    game_night: GameNight = Relationship(back_populates="images")
    
    #has images and sessions linked to it

class GameSessionHelper(SQLModel):
    board_game : BoardGame
    duration_minutes: int | None = None
    winners_user_id: list[int | None] = []

class GameSessionCreate(SQLModel):
    board_game_id: int
    duration_minutes: int | None = None
    winner_user_ids: list[int] = []

class GameNightCreate(SQLModel):
    host_user_id: int
    description: str | None = None
    images: list[str] = []
    sessions: list[GameSessionCreate] = []
    users: list[int] = []



    

class GameNightPublic(SQLModel):
    id: Optional[int] = None
    host_user_id: int
    game_night_date: Optional[date] = None
    description: Optional[str] = None
    sessions: List[GameSessionHelper] = []
    images: List[str] = []
    users: List[UserBoardGamePublic] = []