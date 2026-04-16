from sqlmodel import Field, SQLModel


class UserBlockLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="userboardgame.id", primary_key=True)
    blocked_user_id: int = Field(foreign_key="userboardgame.id", primary_key=True)
