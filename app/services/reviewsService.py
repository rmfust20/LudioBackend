


from app.connection import SessionDep
from app.models import Review
from sqlmodel import Session, select



def insert_review_for_board_game(review: Review, session: SessionDep) -> Review:
    session.add(review)
    session.commit()
    session.refresh(review)
    
    return review

def getReviewStats(board_game_id: int, session: SessionDep) -> float | None:
    statement = select(Review).where(Review.board_game_id == board_game_id)
    reviews = session.exec(statement).all()
    
    if not reviews:
        return None
    
    total_rating = sum(review.rating for review in reviews if review.rating is not None)
    count = sum(1 for review in reviews if review.rating is not None)
    
    if count == 0:
        return None
    
    average_rating = total_rating / count
    number_of_ratings = sum(1 for review in reviews if review.rating is not None)
    number_of_reviews = sum(1 for review in reviews if review.comment is not None)

    return (average_rating,number_of_ratings,number_of_reviews)


