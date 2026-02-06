from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from app.connection import SessionDep
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import Review, UserBoardGame, ReviewUpdate
from app.services import getBoardGameByName, reviewsService
from app.services.userService import get_current_user


router = APIRouter(
    prefix="/reviews",
)

@router.get("/boardGame/{board_game_id}", response_model=list[Review])
def read_reviews_by_board_game_name(board_game_id, session: SessionDep):     #consider how this is ordered later -> by date created desc? popularity?
    statement = select(Review).where(Review.board_game_id == board_game_id).order_by(Review.id).limit(25)

    reviews = session.exec(statement).all()
    
    return reviews

@router.get("/reviewStats/{board_game_id}")
def read_computed_average_rating(board_game_id:int, session:SessionDep):
    stats = reviewsService.getReviewStats(board_game_id, session)
    if stats is None:
        raise HTTPException(404, "No reviews found for this board game")
    return {"average_rating": stats[0], "number_of_ratings": stats[1], "number_of_reviews": stats[2]}



@router.post("/postReview", response_model=Review)
def create_review_for_board_game(review: Review, session: SessionDep, 
                                 user: UserBoardGame = Depends(get_current_user)): 
    #do need to ensure that the userID is the same as the authenticated user
    if review.user_id != user.id:
        raise HTTPException(403, "Cannot create review for another user")
    return reviewsService.insert_review_for_board_game(review, session)

@router.patch("/editReview/{review_id}", response_model=ReviewUpdate)
def edit_review_for_board_game(review_id:int, updated_review: ReviewUpdate, session: SessionDep):
    statement = select(Review).where(Review.id == review_id)
    existing_review = session.exec(statement).first()
    if not existing_review:
        raise HTTPException(404, "Review not found")
    
    data = updated_review.model_dump(exclude_unset=True)
    existing_review.sqlmodel_update(data)

    
    
    session.add(existing_review)
    session.commit()
    session.refresh(existing_review)
    
    return existing_review

@router.get("/userBoardGame/{user_id}/{board_game_id}", response_model=Review | None)
def get_user_review_for_board_game(user_id:int, board_game_id:int, session:SessionDep):
    statement = select(Review).where(Review.user_id == user_id, Review.board_game_id == board_game_id).order_by(Review.id .desc())
    review = session.exec(statement).first()
    return review




    