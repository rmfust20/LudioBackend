from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.connection import engine
import app.models
from app.models import UserBoardGame, UserBoardGameCreate, UserBoardGamePublic, UserBoardGameUpdate, GameNight, GameSession
from app.routes import boardGameAPI
from app.routes import reviewsAPI
from app.routes import userAPI
from app.routes import gameNightAPI
from app.routes import imagesAPI


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
app.include_router(boardGameAPI.router)
app.include_router(reviewsAPI.router)
app.include_router(userAPI.router)
app.include_router(gameNightAPI.router)
app.include_router(imagesAPI.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()









'''
@app.get("/")
def populate(session: SessionDep):
    create_board_games(session)
    return {"message": "Database populated with board games."}
'''






