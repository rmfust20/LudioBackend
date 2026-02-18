from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Date, Field, Relationship, SQLModel

if TYPE_CHECKING:
    # This only runs during static analysis (IDE/Mypy), not at runtime
    from app.models.gameSession import GameSession

class GameNight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    host_user_id: int = Field(foreign_key="userboardgame.id", index=True)

    date: Optional[Date] = None
    description: Optional[str] = None

    # IMPORTANT: default_factory=list
    sessions: list["GameSession"] = Relationship(back_populates="game_night")

    images: list["GameNightImage"] = Relationship(back_populates="game_night")

class GameNightImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    image_url: Optional[str] = None

    game_night: GameNight = Relationship(back_populates="images")
    
    #has images and sessions linked to it

class GameSessionHelper(SQLModel):
    board_game_id: int
    duration_minutes: int | None = None
    winner_user_id: int | None = None
    images: list[str] | None = None
    users: list[int] | None = None

class GameNightPublic(SQLModel):
    host_user_id: int
    date: Optional[str] = None
    description: Optional[str] = None
    sessions: List[GameSessionHelper] = []
    images: List[str] = []
    user_ids: List[int] = []
