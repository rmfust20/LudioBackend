from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.gameNight import GameNight  # only for type hints


class GameSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    board_game_id: int = Field(foreign_key="boardgame.id", index=True)
    duration_minutes: int | None = Field(default=None)
    winner_user_id: int | None = Field(default=None, foreign_key="userboardgame.id", index=True)


    game_night: Optional["GameNight"] = Relationship(back_populates="sessions")

    images: List["GameSessionImage"] = Relationship(
        back_populates="game_session",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    #Subsection of GameNight, has images and users linked to it

class GameSessionPublic(SQLModel):
    id: int
    game_night_id: int
    board_game_id: int
    duration_minutes: int | None = None
    winner_user_id: int | None = None
    images: list[str] | None = None
    users: list[int] | None = None

class GameSessionImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_session_id: int = Field(foreign_key="gamesession.id", index=True)
    image_url: str | None = Field(default=None)
    game_session: "GameSession" = Relationship(back_populates="images")