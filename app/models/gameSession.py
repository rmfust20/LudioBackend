from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Date, Field, Relationship, SQLModel
from datetime import date
from app.models.gameSessionUserLink import GameSessionUserLink
from app.models.boardGame import BoardGame

if TYPE_CHECKING:
    # This only runs during static analysis (IDE/Mypy), not at runtime
    from app.models.gameNight import GameNight
    from app.models.user import UserBoardGame




class GameSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    board_game_id: int = Field(foreign_key="boardgame.id", index=True)
    duration_minutes: int | None = Field(default=None)
    session_date: date | None = Field(default=None)
    game_night: "GameNight" = Relationship(back_populates="sessions")
    winners: list["UserBoardGame"] = Relationship(back_populates="won_sessions", link_model=GameSessionUserLink)
    board_game: BoardGame = Relationship()
    #Subsection of GameNight, has images and users linked to it

class GameSessionPublic(SQLModel):
    game_night_id: int
    board_game_id: int
    duration_minutes: int | None = None
    winners_user_id: list[int | None] = []