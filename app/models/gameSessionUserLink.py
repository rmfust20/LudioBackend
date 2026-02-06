from sqlmodel import Field, Session, SQLModel, create_engine, select


class GameSessionUserLink(SQLModel, table=True):
    game_session_id: int = Field(foreign_key="gamesession.id", primary_key=True)
    user_id: int = Field(foreign_key="userboardgame.id", primary_key=True)