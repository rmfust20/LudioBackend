from sqlmodel import Field, Session, SQLModel, create_engine, select


class GameNightUserLink(SQLModel, table=True):
    game_night_id: int = Field(foreign_key="gamenight.id", primary_key=True)
    user_id: int = Field(foreign_key="userboardgame.id", primary_key=True)