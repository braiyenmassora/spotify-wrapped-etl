# src/jobs/load.py

import pandas as pd
from pathlib import Path
from src.common.config import Config


def save_raw(df: pd.DataFrame, filename: str) -> None:
    """save dataframe to raw data folder."""
    path = Path(Config.RAW_DATA_PATH)
    path.mkdir(parents=True, exist_ok=True)

    filepath = path / f"{filename}.parquet"
    df.to_parquet(filepath, index=False)
    print(f"saved {filename}.parquet to {filepath}")


def save_processed(df: pd.DataFrame, filename: str) -> None:
    """save dataframe to processed data folder."""
    path = Path(Config.PROCESSED_DATA_PATH)
    path.mkdir(parents=True, exist_ok=True)

    filepath = path / f"{filename}.parquet"
    df.to_parquet(filepath, index=False)
    print(f"saved {filename}.parquet to {filepath}")


if __name__ == "__main__":
    # load processed data from transform output
    genre_summary = pd.read_parquet(
        f"{Config.PROCESSED_DATA_PATH}/genre_summary.parquet"
    )
    tracks_clean = pd.read_parquet(
        f"{Config.PROCESSED_DATA_PATH}/top_tracks_clean.parquet"
    )

    save_processed(genre_summary, "genre_summary")
    save_processed(tracks_clean, "top_tracks_clean")
