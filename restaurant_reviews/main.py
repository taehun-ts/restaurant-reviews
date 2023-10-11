import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

"""
# 안양 사무실 주변 식당 리얼 후기
"""
df = pd.read_csv("https://raw.githubusercontent.com/taehun-ts/restaurant-reviews/main/restaurant.csv")
colors = np.random.rand(len(df), 3).tolist()
colors = list(
    map(
        lambda x: "{:02x}{:02x}{:02x}".format(
            int(255 * x[0]),
            int(255 * x[1]),
            int(255 * x[2]),
        ),
        colors,
    ),
)
df.insert(loc=0, column="color", value=colors)


def color_restaurant(val):
    return "background-color: #{};".format(val)


mapstyle = st.sidebar.selectbox(
    "Choose Map Style:",
    options=["light", "dark", "satellite", "road"],
    format_func=str.capitalize,
)


def hex_to_rgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


df["color_rgb"] = df["color"].apply(hex_to_rgb)

st.pydeck_chart(
    pdk.Deck(
        map_style=f"{mapstyle}",  # 'light', 'dark', 'satellite', 'road'
        initial_view_state=pdk.ViewState(
            latitude=df.iloc[0]["lat"],
            longitude=df.iloc[0]["lon"],
            zoom=16,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[lon, lat]",
                get_color="[color_rgb[0], color_rgb[1], color_rgb[2]]",
                get_radius=5,
            ),
        ],
    )
)

st.dataframe(df.style.map(color_restaurant, subset=["color"]))
