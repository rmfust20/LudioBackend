#This service will retrieve a boardgame by name
#we will be given some name that the user has sent us

#first we will query our database to see if we have it and if we don't we will check bgg
import time
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
from app.utilities import fuzzy
from app.models.boardGameDesigner import BoardGameDesigner
from app.models.boardGameDesignerLink import BoardGameDesignerLink
import requests
import xmltodict
import os
from dotenv import load_dotenv


def get_board_game_by_name(name: str, session: SessionDep):
    statement = select(BoardGame).where(BoardGame.name.ilike(f'%{name}%'))
    board_games = session.exec(statement).all()
    print(board_games)
    if len(board_games) < 1:
        #check if bgg has it
        board_games = get_board_game_from_bgg_by_name(name, session)

        if board_games == None:
            raise HTTPException(status_code=404, detail="Board game not found")
    return board_games

def get_board_game_from_bgg_by_name(name_query: str, session: SessionDep) -> list[BoardGame] | None:
    load_dotenv()
    url = f"https://api.geekdo.com/xmlapi2/search?query={name_query}&type=boardgame"

    bearer = os.getenv("bearer_token")

    headers = {
            "Authorization": f"Bearer {bearer}"
        }
    
    r = requests.get(url, headers=headers)

    data = xmltodict.parse(r.text)

    items = data.get("items", {})

    if not items:
        return None
    item_list = []
    relevancy_list = []
    
    #items["item"] is a list of all the dicts that we need to check
    item_list_raw = items["item"]
    if isinstance(item_list_raw, dict):
        item_list_raw = [item_list_raw]
    for item_dict in item_list_raw:
        id = item_dict["@id"]
        name = item_dict["name"]


        if isinstance(name, list) and len(name) > 1:
            name = name[0]
        
        if isinstance(name, dict):
            name = name["@value"]
        else:
            name = name[0]["@value"]
        
        relevancy_list.append((fuzzy.compute_score(name_query, name), id, name))
    
    relevancy_list.sort(key=lambda x: x[0], reverse=True)

    #take the top 5 results and fetch their details from bgg
    top_results = relevancy_list[:5]
    print(top_results)
    results = []

    for thing in top_results:
        print(f"Fetching board game with ID: {thing[1]}")
        board_game = get_board_game_from_bgg_by_id(thing[1], session)
        if board_game != None:
            results.append(board_game)
        
        time.sleep(5)
    
    if len(results) > 0:
        print(results)
        return results
    return None




def get_board_game_from_bgg_by_id(game_id: int, session: SessionDep) -> BoardGame | None:
    existing = session.get(BoardGame, game_id)
    if existing:
        return existing.model_dump()

    load_dotenv()
    url = f"https://api.geekdo.com/xmlapi2/thing?id={game_id}&stats=1"

    bearer = os.getenv("bearer_token")

    headers = {
            "Authorization": f"Bearer {bearer}"
        }
    
    r = requests.get(url, headers=headers)

    data = xmltodict.parse(r.text)

    item = data.get("items", {}).get("item")
    if not item:
        return None

    if item.get("@type") != "boardgame":
        return None
    
    thumbnail = item.get("thumbnail")
    image = item.get("image")
    description = item.get("description")
    year_published = item.get("yearpublished", {}).get("@value")
    min_players = item.get("minplayers", {}).get("@value")
    max_players = item.get("maxplayers", {}).get("@value")
    play_time = item.get("playingtime", {}).get("@value")
    min_age = item.get("minage", {}).get("@value")

    name = item["name"]


    if isinstance(name, list) and len(name) > 1:
        name = name[0]
        
    if isinstance(name, dict):
        name = name["@value"]
    else:
        name = name[0]["@value"]
        
    links = data["items"]["item"]["link"]
    board_game_categories = []
    board_game_mechanics = []
    publishers = []
    board_game_designers = []

    for item in links:
        if item["@type"] == "boardgamecategory":
            board_game_categories.append((item["@value"],item["@id"]))
        elif item["@type"] == "boardgamemechanic":
            board_game_mechanics.append((item["@value"],item["@id"]))
        elif item["@type"] == "boardgamepublisher":
            publishers.append((item["@value"],item["@id"]))
        elif item["@type"] == "boardgamedesigner":
            board_game_designers.append((item["@value"],item["@id"]))
        
    board_game = BoardGame(
        id = game_id,
        name = name,
        thumbnail = thumbnail ,
        image = image,
        year_published = year_published,
        description = description,
        min_players = min_players,
        max_players = max_players,
        play_time = play_time,
        min_age = min_age,
    )

    

    board_game = BoardGame.model_validate(board_game)
    session.add(board_game)
    session.flush()

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
            
        existing_link = session.get(BoardGameCategoryLink, (game_id, category_id))
        if not existing_link:
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
            
        existing_link = session.get(BoardGameMechanicLink, (game_id, mechanic_id))
        if not existing_link:
            link = BoardGameMechanicLink(
                    board_game_id = game_id,
                    mechanic_id = mechanic_id
                )
            link = BoardGameMechanicLink.model_validate(link)
            session.add(link)
            session.flush()

    for designer_name, designer_id in board_game_designers:
        session_designer = session.get(BoardGameDesigner, designer_id)
        if not session_designer:
            session_designer = BoardGameDesigner(
                    id = designer_id,
                    name = designer_name
                )
            session_designer = BoardGameDesigner.model_validate(session_designer)
            session.add(session_designer)
            session.flush()
            
        existing_link = session.get(BoardGameDesignerLink, (game_id, designer_id))
        if not existing_link:
            link = BoardGameDesignerLink(
                    board_game_id = game_id,
                    designer_id = designer_id
                )
            link = BoardGameDesignerLink.model_validate(link)
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
            
        existing_link = session.get(BoardGamePublisherLink, (game_id, publisher_id))
        if not existing_link:
            link = BoardGamePublisherLink(
                    board_game_id = game_id,
                    publisher_id = publisher_id
                )
            link = BoardGamePublisherLink.model_validate(link)
            session.add(link)
            session.flush()

    
    board_game_dict = board_game.model_dump()
    session.commit()
    print(f"Added board game {name} with ID {game_id} to the database.")
    return board_game_dict
    

    


  