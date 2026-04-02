from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from app.connection import SessionDep
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import BoardGame
from app.models.boardGame import BoardGameFeedItem
from app.models.gameNight import GameNight, GameNightPublic, GameNightCreate
from app.services import reviewsService, feedService
from app.models import BoardGameDesigner
from app.models import BoardGameDesignerLink
from app.services import get_game_night_feed
from app.services.gameNightService import add_game_night, get_user_game_night, get_user_game_nights, delete_game_night
from app.models.user import UserBoardGame
from app.services.userService import get_current_user
from app.utilities.limiter import limiter


router = APIRouter(
    prefix="/gameNights",
    )

@router.get("/userFeed/{user_id}", response_model=list[GameNightPublic])
@limiter.limit("300/hour")
def get_game_nights(request: Request, user_id: int, session: SessionDep, offset: int = 0, _: UserBoardGame = Depends(get_current_user)):
    print("logging user id and offset", user_id, offset)
    feed = get_game_night_feed(user_id=user_id, offset=offset, session=session)
    return feed


@router.post("/postNight")
@limiter.limit("20/hour")
def post_game_night(request: Request, game_night_public: GameNightCreate, session: SessionDep, _: UserBoardGame = Depends(get_current_user)):
    add_game_night(payload=game_night_public, session=session)
    return {"message": "Game night added successfully"}

@router.get("/userGameNights/{user_id}", response_model=list[GameNightPublic])
@limiter.limit("300/hour")
def get_user_game_nights_route(request: Request, user_id: int, session: SessionDep, _: UserBoardGame = Depends(get_current_user)):
    return get_user_game_nights(user_id, session)

@router.get("/{game_night_id}", response_model=GameNightPublic)
@limiter.limit("300/hour")
def get_game_night_route(request: Request, game_night_id: int, session: SessionDep, _: UserBoardGame = Depends(get_current_user)):
    night = get_user_game_night(game_night_id, session)
    if not night:
        raise HTTPException(404, "Game night not found")
    return night

@router.delete("/{game_night_id}")
@limiter.limit("60/hour")
def delete_game_night_route(request: Request, game_night_id: int, session: SessionDep, current_user: UserBoardGame = Depends(get_current_user)):
    try:
        found = delete_game_night(game_night_id, current_user.id, session)
    except ValueError:
        raise HTTPException(403, "Not authorized to delete this game night")
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    if not found:
        raise HTTPException(404, "Game night not found")
    return {"message": "Game night deleted"}
