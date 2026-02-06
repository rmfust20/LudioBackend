from requests import session
from app.connection import SessionDep
from app.models import Review, BoardGameDesigner, BoardGameDesignerLink, BoardGame, BoardGameFeedItem
from sqlmodel import Session, select, func, join, case

def get_board_game_feed_item(offset: int, limit: int, session: SessionDep) -> list[BoardGameFeedItem]:
    #I want to query the database such that it returns a list of BoardGameFeedItem
    #So I need to join the BoardGame table with the Review table to get the average rating, number of ratings, number of reviews
    #And i need to join with the BoardGameDesigner and BoardGameDesignerLink tables to get the designers


    review_stats_sq = (
        select(
            Review.board_game_id.label("bg_id"),
            func.count(Review.id).label("number_of_reviews"),
            func.count(Review.rating).label("number_of_ratings"),  # counts non-null ratings
            func.avg(Review.rating).label("average_rating"),       # averages non-null ratings
        )
        .group_by(Review.board_game_id)
    ).subquery()

    designer_sq = (
    select(
        BoardGameDesignerLink.board_game_id.label("bg_id"),
        func.array_agg(BoardGameDesigner.name).label("designers"),
    )
    .join(BoardGameDesigner, BoardGameDesigner.id == BoardGameDesignerLink.designer_id)
    .group_by(BoardGameDesignerLink.board_game_id)
    ).subquery()

    stmt = select(
        BoardGame,
        func.coalesce(review_stats_sq.c.number_of_reviews, 0).label("number_of_reviews"),
        func.coalesce(review_stats_sq.c.number_of_ratings, 0).label("number_of_ratings"),
        review_stats_sq.c.average_rating.label("average_rating"),
        designer_sq.c.designers.label("designers"),  # ✅ no coalesce/cast here
    ).outerjoin(review_stats_sq, review_stats_sq.c.bg_id == BoardGame.id).outerjoin(designer_sq, designer_sq.c.bg_id == BoardGame.id)
    
    rows = session.exec(stmt).all()

    items: list[BoardGameFeedItem] = []
    for bg, num_reviews, num_ratings, avg, designers in rows:
        item = BoardGameFeedItem(
        **bg.model_dump(),
        number_of_reviews=int(num_reviews or 0),
        number_of_ratings=int(num_ratings or 0),
        average_rating=float(avg) if avg is not None else None,
        designers=list(designers) if designers is not None else [],  # ✅ here
    )
        items.append(item)
    
    return items





