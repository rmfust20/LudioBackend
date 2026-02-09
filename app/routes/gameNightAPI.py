from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from app.connection import SessionDep
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import BoardGame
from app.models.boardGame import BoardGameFeedItem
from app.models.gameNight import GameNight
from app.services import getBoardGameByName, reviewsService, feedService
from app.models import BoardGameDesigner
from app.models import BoardGameDesignerLink
from app.services import get_game_night_feed


router = APIRouter(
    prefix="/gameNights",
    )

@router.get("/feed{user_id}", response_model=list[GameNight])
def get_game_nights(user_id: int, session:SessionDep, offset: int = 0):
    get_game_night_feed(user_id=user_id, offset=offset, session=session)
    

    