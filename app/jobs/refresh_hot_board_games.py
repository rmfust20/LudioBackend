#Entrypoint for the ACA Job that refreshes the BGG hot board games list.
#Run as: python -m app.jobs.refresh_hot_board_games

import sys
import traceback
from sqlmodel import Session, SQLModel

import app.models  # noqa: F401 — ensure every table is registered on the metadata
from app.connection.conn import engine
from app.services.getHotBoardGames import get_hot_board_games


def main() -> int:
    #The FastAPI startup hook is what normally runs create_all; this Job
    #bypasses FastAPI entirely, so do it here too. Idempotent — safe to
    #run every invocation.
    SQLModel.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            results = get_hot_board_games(session=session)
    except Exception as e:
        print(f"[refresh_hot_board_games] failed: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        return 1

    if not results:
        print("[refresh_hot_board_games] finished but wrote 0 games", file=sys.stderr, flush=True)
        return 1

    print(f"[refresh_hot_board_games] finished, wrote {len(results)} games", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
