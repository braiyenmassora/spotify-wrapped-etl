# src/common/spotify_client.py

import spotipy
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from spotipy.oauth2 import SpotifyOAuth

from src.common.config import Config


def _build_auth() -> SpotifyOAuth:
    """build spotify oauth instance from config."""
    return SpotifyOAuth(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        redirect_uri=Config.REDIRECT_URI,
        scope=Config.SCOPE,
        cache_path=".spotify_cache",
        open_browser=False,
    )


def _run_auth_server(auth: SpotifyOAuth) -> None:
    """run fastapi server to handle oauth callback then shutdown."""
    app = FastAPI()
    config = uvicorn.Config(app, host="127.0.0.1", port=8889, log_level="warning")
    server = uvicorn.Server(config)

    @app.on_event("startup")
    async def startup() -> None:
        url = auth.get_authorize_url()
        print(f"open this url in your browser:\n{url}\n")

    @app.get("/callback")
    async def callback(code: str) -> HTMLResponse:
        auth.get_access_token(code)
        print("token saved. shutting down auth server...")
        server.should_exit = True
        return HTMLResponse("authorization successful. return to terminal.")

    server.run()


def get_spotify_client() -> spotipy.Spotify:
    """
    return authenticated spotify client.

    flow:
    - token cached  -> connect directly
    - token missing -> run fastapi auth server then continue
    """
    auth = _build_auth()
    token = auth.get_cached_token()

    if not token:
        print("no token found. starting auth server...")
        _run_auth_server(auth)

    client = spotipy.Spotify(auth_manager=auth)

    user = client.current_user()
    if user:
        print(f"connected as: {user['display_name']}")  # type: ignore
    else:
        raise Exception("failed to get user info")

    return client
