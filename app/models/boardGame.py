from sqlmodel import Field, SQLModel

class BoardGameBase(SQLModel):
    id: int
    name: str
    thumbnail: str | None = None
    play_time: int | None = None
    min_players: int | None = None
    max_players: int | None = None
    year_published: int | None = None
    description: str | None = None
    min_age: int | None = None
    image: str | None = None


class BoardGame(BoardGameBase, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)


class BoardGameFeedItem(BoardGameBase):  # ✅ NOT a table
    feed_position: int | None = None
    average_rating: float | None = None
    number_of_ratings: int = 0
    number_of_reviews: int = 0
    designers: list[str] = Field(default_factory=list)
