# src/jobs/transform.py

import pandas as pd
from src.transform.genre import transform_genre
from src.transform.track import transform_tracks
from src.jobs.load import save_processed


if __name__ == "__main__":
    # read raw data
    artists = pd.read_parquet("data/raw/top_artists.parquet")
    tracks = pd.read_parquet("data/raw/top_tracks.parquet")

    # transform
    genre_summary = transform_genre(artists)
    tracks_clean = transform_tracks(tracks)

    # save processed
    save_processed(genre_summary, "genre_summary")
    save_processed(tracks_clean, "top_tracks_clean")
