from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models.boardGame import BoardGame
from app.models.boardGameCategory import BoardGameCategory
from app.models.boardGameMechanic import BoardGameMechanic
from app.models.boardGameCategoryLink import BoardGameCategoryLink
from app.models.boardGameMechanicLink import BoardGameMechanicLink
from app.models.publisher import Publisher
from app.models.boardGamePublisherLink import BoardGamePublisherLink
from app.connection.conn import SessionDep
import time
import requests
import xmltodict
import os
import random
from dotenv import load_dotenv



def create_board_games(session: SessionDep):
    load_dotenv()

    used_ids = set()

    for i in range(1,1000):
        game_id = random.randint(1,50000)
        while game_id in used_ids:
            game_id = random.randint(1,50000)
        used_ids.add(game_id)
        url = f"https://api.geekdo.com/xmlapi2/thing?id={game_id}&stats=1"

        bearer = os.getenv("bearer_token")

        headers = {
            "Authorization": f"Bearer {bearer}"
        }

        r = requests.get(url, headers=headers)
        time.sleep(3)

        data = xmltodict.parse(r.text)

        item = data.get("items", {}).get("item")
        if not item:
            continue

        if item.get("@type") != "boardgame":
            continue
        # Save if it's a boardgame ite

        try:
            thumbnail = item.get("thumbnail")
            image = item.get("image")
            year_published = (item.get("yearpublished") or {}).get("@value")
            description = item.get("description")
            min_players = (item.get("minplayers") or {}).get("@value")
            max_players = (item.get("maxplayers") or {}).get("@value")
            play_time = (item.get("playingtime") or {}).get("@value")
            min_age = (item.get("minage") or {}).get("@value")

            name = item.get("name")
            if not name:
                continue
            if isinstance(name, list):
                name = name[0]
            if isinstance(name, dict):
                name = name.get("@value")
            if not name:
                continue

            links = item.get("link", [])
            if isinstance(links, dict):
                links = [links]
        except Exception as e:
            continue

        board_game_categories = []
        board_game_mechanics = []
        publishers = []

        for item in links:
            if item["@type"] == "boardgamecategory":
                board_game_categories.append((item["@value"],item["@id"]))
            elif item["@type"] == "boardgamemechanic":
                board_game_mechanics.append((item["@value"],item["@id"]))
            elif item["@type"] == "boardgamepublisher":
                publishers.append((item["@value"],item["@id"]))
        
        try:
            board_game = BoardGame(
                id = game_id,
                name = name,
                thumbnail = thumbnail,
                image = image,
                year_published = year_published,
                description = description,
                min_players = min_players,
                max_players = max_players,
                play_time = play_time,
                min_age = min_age
            )

            board_game = BoardGame.model_validate(board_game)
            session.add(board_game)
            session.flush()
        except Exception as e:
            session.rollback()
            continue

        for category_name, category_id in board_game_categories:
            sessiongame_category = session.get(BoardGameCategory, category_id)
            if not sessiongame_category:
                sessiongame_category = BoardGameCategory(
                    id = category_id,
                    name = category_name
                )
                sessiongame_category = BoardGameCategory.model_validate(sessiongame_category)
                session.add(sessiongame_category)
                session.flush()
            
            link = BoardGameCategoryLink(
                board_game_id = game_id,
                category_id = category_id
            )

            link = BoardGameCategoryLink.model_validate(link)
            session.add(link)
            session.flush()
        
        for mechanic_name, mechanic_id in board_game_mechanics:
            sessiongame_mechanic = session.get(BoardGameMechanic, mechanic_id)
            if not sessiongame_mechanic:
                sessiongame_mechanic = BoardGameMechanic(
                    id = mechanic_id,
                    name = mechanic_name
                )
                sessiongame_mechanic = BoardGameMechanic.model_validate(sessiongame_mechanic)
                session.add(sessiongame_mechanic)
                session.flush()
            
            link = BoardGameMechanicLink(
                board_game_id = game_id,
                mechanic_id = mechanic_id
            )

            link = BoardGameMechanicLink.model_validate(link)
            session.add(link)
            session.flush()
        
        for publisher_name, publisher_id in publishers:
            session_publisher = session.get(Publisher, publisher_id)
            if not session_publisher:
                session_publisher = Publisher(
                    id = publisher_id,
                    name = publisher_name
                )
                session_publisher = Publisher.model_validate(session_publisher)
                session.add(session_publisher)
                session.flush()
            
            link = BoardGamePublisherLink(
                board_game_id = game_id,
                publisher_id = publisher_id
            )

            link = BoardGamePublisherLink.model_validate(link)
            session.add(link)
            session.flush()
        
        session.commit()




        

        #ok so now we have all the data extracted from one game
        #we now need to insert into 5 different tables
        #board_game, board_game_category, board_game_mechanic, publisher
        #and the association tables

        #ok so now when we are sending to the tables
        #straight send the new boardgame in
        #check if the category/mechanic/publisher exists first
        #if not, insert it, then get the id
        #then insert into the association table

        




        time.sleep(10)  # prevent throttling