# dashboard/app.py

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts  # type: ignore

st.set_page_config(
    page_title="Spotify Wrapped",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0e0e0e;
        color: #f0f0f0;
    }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
        color: #f0f0f0;
    }

    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }

    .metric-label {
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 22px;
        font-weight: 500;
        color: #f0f0f0;
    }

    .section-label {
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #888;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    tracks = pd.read_parquet("data/processed/top_tracks_clean.parquet")
    genres = pd.read_parquet("data/processed/genre_summary.parquet")
    return tracks, genres


tracks, genres = load_data()
top10_genres = genres.head(10)

# header
st.markdown("<p class='section-label'>year in music</p>", unsafe_allow_html=True)
st.title("Spotify Wrapped")
st.caption(
    "a summary of listening habits over the last 6 months, "
    "based on top 50 tracks and artists pulled from the Spotify API."
)
st.divider()

# metric cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>Top Genre</div>
            <div class='metric-value'>{genres.iloc[0]['genres'].title()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>Top Artist</div>
            <div class='metric-value'>{tracks.iloc[0]['artist']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>Top Track</div>
            <div class='metric-value'>{tracks.iloc[0]['name']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# layout: kiri = genre chart, kanan = top tracks
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Top Genres")
    st.caption(
        "genres are extracted from the top 50 artists. "
        "since one artist can belong to multiple genres, "
        "the count reflects how often each genre appears across all top artists."
    )

    genre_options = {
        "tooltip": {"trigger": "axis"},
        "grid": {"left": "3%", "right": "10%", "containLabel": True},
        "xAxis": {
            "type": "value",
            "axisLine": {"lineStyle": {"color": "#2a2a2a"}},
            "splitLine": {"lineStyle": {"color": "#1a1a1a"}},
            "axisLabel": {"color": "#888"},
        },
        "yAxis": {
            "type": "category",
            "data": top10_genres["genres"].tolist(),
            "axisLine": {"lineStyle": {"color": "#2a2a2a"}},
            "axisLabel": {"color": "#f0f0f0"},
        },
        "series": [
            {
                "type": "bar",
                "data": top10_genres["count"].tolist(),
                "itemStyle": {"color": "#f0f0f0", "borderRadius": [0, 6, 6, 0]},
                "label": {
                    "show": True,
                    "position": "right",
                    "color": "#888",
                    "formatter": "{c}x",
                },
            }
        ],
        "backgroundColor": "#0e0e0e",
    }

    st_echarts(options=genre_options, height="380px")

with col_right:
    st.subheader("Top Tracks")
    st.caption(
        "most played tracks over the last 6 months, ranked by popularity score (0-100). "
        "popularity is calculated by Spotify based on total streams and how recent those streams are."
    )
    st.dataframe(
        tracks[["rank", "name", "artist", "album", "duration", "popularity"]],
        use_container_width=True,
        hide_index=True,
    )
