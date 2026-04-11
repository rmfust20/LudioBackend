from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class HotBoardGame(SQLModel, table=True):
    board_game_id: int = Field(foreign_key="boardgame.id", primary_key=True)
    rank: int = Field(index=True)
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
