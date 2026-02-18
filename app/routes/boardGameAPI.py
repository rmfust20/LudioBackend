from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from app.connection import SessionDep
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import BoardGame
from app.models.boardGame import BoardGameFeedItem
from app.services import getBoardGameByName, reviewsService, feedService, get_general_trending_feed
from app.models import BoardGameDesigner
from app.models import BoardGameDesignerLink
from app.services.boardGameService import get_trending_with_friends_feed


router = APIRouter(
    prefix="/boardGames",
)

#search for a board game by name - if not found populates from BGG to our database
@router.get("/search/{name}", response_model=list[BoardGame])
def read_board_game_by_name(name : str,session: SessionDep):
    board_games = getBoardGameByName.get_board_game_by_name(name, session)
    if board_games == None:
        raise HTTPException(status_code=404, detail="Board game not found")
    return board_games

@router.get("/userFeed/{user_id}", response_model=list[BoardGame])
def get_user_board_games_feed(user_id: int, session:SessionDep, lastSeenID : int = 0):
    #we want to return a feed of board games for the user
    #for now, just return all board games with id > lastSeenID ordered by id
    statement = select(BoardGame).offset(lastSeenID).order_by(BoardGame.id).limit(25)
    board_games = session.exec(statement).all()
    return board_games

@router.get("/userFeed/{user_id}/rehydrate", response_model=list[BoardGame])
def rehydrate_user_board_games(user_id: int, session:SessionDep, board_game_ids: list[int] = Query(...)):
    statement = select(BoardGame).where(BoardGame.id.in_(board_game_ids)).order_by(BoardGame.id)
    board_games = session.exec(statement).all()
    return board_games

@router.get("/trendingFeed", response_model=list[BoardGame])
def get_trending_board_games_feed(session:SessionDep,offset: int = 0):
    return get_general_trending_feed(session=session, offset=offset)

@router.get("/trendingFriends/{user_id}", response_model=list[BoardGame])
def get_trending_friends_board_games_feed(user_id: int, session:SessionDep, offset: int = 0):
    return get_trending_with_friends_feed(user_id=user_id, session=session, offset=offset)

#Deprecated
@router.get("/feed", response_model=list[BoardGame])
def get_board_games(session:SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    board_games = select(BoardGame).offset(offset).limit(limit)
    boardGames = session.exec(board_games).all()
    return boardGames

#get indidual board game by id
@router.get("/fetchBoardGame/{board_game_id}", response_model=BoardGame)
def get_board_game_by_id(board_game_id: int, session:SessionDep):
    statemenet = select(BoardGame).where(BoardGame.id == board_game_id)
    board_game = session.exec(statemenet).first()   
    if board_game == None:
        raise HTTPException(status_code=404, detail="Board game not found")
    return board_game

#get designers
@router.get("/designers/{board_game_id}", response_model=list[BoardGameDesigner])
def get_board_game_designers(board_game_id: int, session:SessionDep):
    statement = (
        select(BoardGameDesigner)
        .join(BoardGameDesignerLink)
        .where(BoardGameDesignerLink.board_game_id == board_game_id)
    )
    results = session.exec(statement).all()
    return results



    