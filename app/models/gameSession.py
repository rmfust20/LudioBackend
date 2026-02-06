from sqlmodel import Field, SQLModel

class GameSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    board_game_id: int = Field(foreign_key="boardgame.id", index=True)
    duration_minutes: int | None = Field(default=None)
    winner_user_id: int | None = Field(default=None, foreign_key="userboardgame.id", index=True)
    #Subsection of GameNight, has images and users linked to it