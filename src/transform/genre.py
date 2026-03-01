# src/transform/genre.py

import pandas as pd


def transform_genre(df: pd.DataFrame) -> pd.DataFrame:
    """transform genres list into frequency summary."""
    genre = df.explode("genres")
    genre = genre[genre["genres"].notna()]
    genre = genre[genre["genres"] != ""]

    # count frequency of every genre
    genre_count = (
        genre.groupby("genres")
        .size()
        .reset_index(name="count")
        .sort_values(
            "count", ascending=False
        )  # fix: "counts" -> "count", "accending" -> "ascending", "FaLSE" -> "False"
    )

    # calculate percentage
    total = genre_count["count"].sum()
    genre_count["percentage"] = (genre_count["count"] / total * 100).round(2)

    print(f"found {len(genre_count)} unique genres.")
    return genre_count
