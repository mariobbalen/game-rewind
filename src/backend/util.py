"""
Precisa do Client ID e Client Secret da twitch (https://dev.twitch.tv/console/apps).
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# busca do env
CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]

# verifica se tem acesso a api (se as credencias estão ok)
def get_access_token() -> str:
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]

# pega a arte da capa
def cover_url(image_id: str, size: str = "cover_big") -> str:
    return f"https://images.igdb.com/igdb/image/upload/t_{size}/{image_id}.jpg"

# faz a busca dos jogos na api e pega a capa de cada um deles
def search_games(query: str, access_token: str) -> list[dict]:
    response = requests.post(
        "https://api.igdb.com/v4/games",
        headers={
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {access_token}",
        },
        # aquilo que vai ser buscado na api
        data=f'search "{query}"; fields name,rating,first_release_date,cover.image_id; limit 100;',
    )
    response.raise_for_status()
    games = response.json()

    # pega a capa para mostrar ao buscar os jogos
    for game in games:
        cover = game.pop("cover", None)
        if cover:
            game["cover_url"] = cover_url(cover["image_id"])

    return games
