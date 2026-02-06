from sqlmodel import Field, SQLModel

class GameSessionImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_session_id: int = Field(foreign_key="gamesession.id", index=True)
    image_url: str | None = Field(default=None)