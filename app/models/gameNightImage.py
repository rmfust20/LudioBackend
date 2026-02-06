from sqlmodel import Field, SQLModel

class GameNightImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_night_id: int = Field(foreign_key="gamenight.id", index=True)
    image_url: str | None = Field(default=None)
    #image for gameNight can be retrieved by GameNightID