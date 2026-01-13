from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.connection import engine
from app.models import UserBoardGame, UserBoardGameCreate, UserBoardGamePublic, UserBoardGameUpdate
from app.routes import boardGameAPI
from app.routes import reviewsAPI
from app.routes import userAPI

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


"""
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


"""






'''
@app.get("/")
def populate(session: SessionDep):
    create_board_games(session)
    return {"message": "Database populated with board games."}
'''






