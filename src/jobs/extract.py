# src/jobs/extract.py
import pandas as pd  # type: ignore
from src.common.client import get_spotify_client
from src.common.config import Config
from src.jobs.load import save_raw


def extract_top_artists() -> pd.DataFrame:
    """extract top artists from spotify."""
    sp = get_spotify_client()

    results = sp.current_user_top_artists(
        limit=Config.LIMIT,
        time_range=Config.TIME_RANGE,
    )

    artists = []
    for item in results["items"]:  # type: ignore
        artists.append(
            {
                "id": item["id"],
                "name": item["name"],
                "genres": item["genres"],
                "popularity": item["popularity"],
                "followers": item["followers"]["total"],
            }
        )

    df = pd.DataFrame(artists)
    print(f"extracted {len(df)} artists.")
    return df


def extract_top_tracks() -> pd.DataFrame:
    """extract top tracks from spotify."""
    sp = get_spotify_client()

    results = sp.current_user_top_tracks(
        limit=Config.LIMIT,
        time_range=Config.TIME_RANGE,
    )

    tracks = []
    for item in results["items"]:  # type: ignore
        duration_ms = item["duration_ms"]
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000

        tracks.append(
            {
                "id": item["id"],
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "artist_id": item["artists"][0]["id"],
                "album": item["album"]["name"],
                "popularity": item["popularity"],
                "duration": f"{minutes}:{seconds:02d}",
            }
        )

    df = pd.DataFrame(tracks)
    print(f"extracted {len(df)} tracks.")
    return df


if __name__ == "__main__":
    artists = extract_top_artists()
    save_raw(artists, "top_artists")

    tracks = extract_top_tracks()
    save_raw(tracks, "top_tracks")
