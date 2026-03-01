# src/transform/tracks.py

import pandas as pd


def transform_tracks(df: pd.DataFrame) -> pd.DataFrame:
    """transform top tracks data."""

    # sort by popularity
    df = df.sort_values("popularity", ascending=False).reset_index(drop=True)

    # add rank column
    df["rank"] = df.index + 1

    print(f"transformed {len(df)} tracks.")
    return df
