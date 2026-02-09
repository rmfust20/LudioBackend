from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.gameSession import GameSession, GameSessionPublic



class GameNight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    host_user_id: int = Field(foreign_key="userboardgame.id", index=True)
    host_username: str = Field(index=True)

    date: Optional[str] = None
    description: Optional[str] = None

    # IMPORTANT: default_factory=list
    sessions: List["GameSession"] = Relationship(
        back_populates="game_night",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    images: List["GameNightImage"] = Relationship(
        back_populates="game_night",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

class GameNightImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    image_url: Optional[str] = None

    game_night: Optional["GameNight"] = Relationship(back_populates="images")
    
    #has images and sessions linked to it

class GameNightPublic(SQLModel):
    id: int
    host_user_id: int
    host_username: str
    date: Optional[str] = None
    description: Optional[str] = None
    sessions: Optional[List[GameSessionPublic]] = []
    images: List[str] = []
    user_ids: List[int] = []