# Entrypoint for the bomb bulk game importer.
# Run as: python -m app.jobs.bomb_board_games
#
# Optional env vars:
#   BOMB_COUNT — number of top-ranked games to fetch (default 1000)

import os
import sys
import traceback
from sqlmodel import Session, SQLModel

import app.models  # noqa: F401 — register all tables
from app.connection.conn import engine
from app.services.bombBoardGames import bomb_board_games


def main() -> int:
    SQLModel.metadata.create_all(engine)

    count = int(os.getenv("BOMB_COUNT", "1000"))

    print(f"[bomb_board_games] starting — fetching top {count} ranked games")

    try:
        with Session(engine) as session:
            added = bomb_board_games(session, count=count)
    except Exception as e:
        print(f"[bomb_board_games] failed: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        return 1

    if added == 0:
        print("[bomb_board_games] finished but added 0 games", file=sys.stderr, flush=True)
        return 1

    print(f"[bomb_board_games] finished, added {added} games", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
