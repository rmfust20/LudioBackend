from sqlmodel import Field, Session, SQLModel, create_engine, select

class UserBoardGameBase(SQLModel):
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    email: str = Field(index = True)

class UserBoardGame(UserBoardGameBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash : str

class UserBoardGamePublic(UserBoardGameBase):
    id: int

class UserBoardGameCreate(UserBoardGameBase):
    password : str

class UserBoardGameUpdate(UserBoardGameBase):
    password: str | None = None

