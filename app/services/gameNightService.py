from requests import session
from sqlalchemy.orm import selectinload
from sqlmodel import select
from app.connection import SessionDep
from app.models import Review, BoardGameDesigner, BoardGameDesignerLink, BoardGame, BoardGameFeedItem
from sqlmodel import Session, select, func, join, case
from app.models.gameNight import GameNight, GameNightPublic, GameNightImage
from app.models.gameNightUserLink import GameNightUserLink
from app.models.gameSession import GameSession, GameSessionImage
from app.models.gameSessionUserLink import GameSessionUserLink

def get_game_night_feed(user_id: int, offset: int, session: SessionDep):
    stmt = (
        select(GameNight)
        .join(GameNightUserLink, GameNight.id == GameNightUserLink.game_night_id)
        .where(GameNightUserLink.user_id == user_id)
        .options(
            selectinload(GameNight.images),                         # night.images
            selectinload(GameNight.sessions).selectinload(GameSession.images),  # night.sessions + session.images
        )
        .order_by(GameNight.date.desc())
        .offset(offset)
        .limit(25)
    )

    nights = session.exec(stmt).unique().all()

    for night in nights:
        print(night)


def add_game_night(payload: GameNightPublic, session: SessionDep):
    # 1) Create the night
    game_night_db = GameNight(
        host_user_id=payload.host_user_id,
        host_username=payload.host_username,
        date=payload.date,
        description=payload.description
    )
    session.add(game_night_db)
    session.flush()  # assigns game_night_db.id

    # 2) Night images
    for url in payload.images:
        session.add(GameNightImage(game_night_id=game_night_db.id, image_url=url))

    # 3) Sessions + their images
    for s in payload.sessions:
        game_session_db = GameSession(
            game_night_id=game_night_db.id,
            board_game_id=s.board_game_id,
            duration_minutes=s.duration_minutes,
            winner_user_id=s.winner_user_id,   # whatever your field name is
            description=s.description
        )
        session.add(game_session_db)
        session.flush()  # assigns game_session_db.id (needed for session images)

        # If your session DTO includes images:
        for url in s.images:
            session.add(GameSessionImage(game_session_id=game_session_db.id, image_url=url))

        for user in s.users:
            session.add(GameSessionUserLink(game_session_id=game_session_db.id, user_id=user.user_id, username=user.username))

    session.commit()
    session.refresh(game_night_db)
    return game_night_db


        





