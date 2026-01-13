from fastapi import Depends
from sqlmodel import Session, create_engine
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv(override=False)  # <- key change

DATABASE_URL = os.getenv("database_url_azure")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
