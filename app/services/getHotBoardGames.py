#This service retrieves the current hot board games from BGG,
#hydrates any that aren't already in our database using the existing
#by-id fetcher, and then wipes and rewrites the HotBoardGame table
#with the new ranked list.

import time
import os
import requests
import xmltodict
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlmodel import delete

from app.models.boardGame import BoardGame
from app.models.hotBoardGame import HotBoardGame
from app.connection.conn import SessionDep
from app.services.getBoardGameByName import get_board_game_from_bgg_by_id


def get_hot_board_games(session: SessionDep):
    load_dotenv()
    url = "https://api.geekdo.com/xmlapi2/hot?type=boardgame"

    bearer = os.getenv("bearer_token")
    headers = {
        "Authorization": f"Bearer {bearer}"
    }

    r = requests.get(url, headers=headers)
    data = xmltodict.parse(r.text)

    items = data.get("items", {})
    if not items or "item" not in items:
        print("[get_hot_board_games] no items returned from BGG")
        return None

    hot_items = items["item"]
    if isinstance(hot_items, dict):
        hot_items = [hot_items]

    #hydrate every game first; only touch the hot table after all fetches
    #succeed so a mid-run failure leaves yesterday's hot list in place.
    hydrated: list[tuple[int, int]] = []  # (rank, game_id)

    for hot_item in hot_items:
        game_id = int(hot_item["@id"])
        rank = int(hot_item["@rank"])
        print(f"[get_hot_board_games] processing rank {rank} id {game_id}")

        existing = session.get(BoardGame, game_id)
        if existing:
            hydrated.append((rank, game_id))
            continue

        board_game = get_board_game_from_bgg_by_id(game_id, session)
        if board_game is not None:
            hydrated.append((rank, game_id))

        time.sleep(5)

    if not hydrated:
        print("[get_hot_board_games] nothing hydrated, leaving hot table untouched")
        return None

    #atomic wipe + rewrite of the hot table
    session.exec(delete(HotBoardGame))
    fetched_at = datetime.now(timezone.utc)
    for rank, game_id in hydrated:
        session.add(HotBoardGame(
            board_game_id=game_id,
            rank=rank,
            fetched_at=fetched_at,
        ))
    session.commit()

    print(f"[get_hot_board_games] wrote {len(hydrated)} hot entries")
    return hydrated
