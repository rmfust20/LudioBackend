from sqlmodel import Field, SQLModel

class GameNight(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    host_user_id: int = Field(foreign_key="userboardgame.id", index=True)
    date: str | None = Field(default=None)
    description: str | None = Field(default=None)
    #has images and sessions linked to it