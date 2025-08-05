import streamlit as st
import pandas as pd
import time
import pydeck as pdk
from sklearn.neighbors import KernelDensity
import numpy as np

@st.cache_data
def load_data(OpenData):
    time.sleep(1)
    df = pd.read_csv(OpenData, encoding="utf-8")
    df["GPS座標X"] = pd.to_numeric(df["GPS座標X"], errors="coerce")
    df["GPS座標Y"] = pd.to_numeric(df["GPS座標Y"], errors="coerce")
    df["年"] = pd.to_numeric(df["年"], errors="coerce")
    df["月"] = pd.to_numeric(df["月"], errors="coerce")
    df["日"] = pd.to_numeric(df["日"], errors="coerce")
    df["日期"] = pd.to_datetime({
        "year": df["年"],
        "month": df["月"],
        "day": df["日"]
    }, errors="coerce")


    df["Date"] = df.get("日期", 0)
    df["GPS coordinate X"] = df.get("GPS座標X", 0)
    df["GPS coordinate Y"] = df.get("GPS座標Y", 0)
    df["Deaths"] = df.get("死亡數量", 0)
    df["Injuries"] = df.get("受傷數量", 0)

    return df.dropna(subset=["GPS座標X", "GPS座標Y", "日期"])


OpenData = "OpenData.csv"

try:
    df = load_data(OpenData)

    st.title("Traffic Accident Data Analysis Dashboard")

    min_date = df["日期"].min()
    max_date = df["日期"].max()

    date_range = st.date_input("Please select a date range：", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df["日期"] >= pd.to_datetime(start_date)) & (df["日期"] <= pd.to_datetime(end_date))]


        df_display = df_filtered[[
            "Date",
            "GPS coordinate X",
            "GPS coordinate Y",
            "Deaths",
            "Injuries"
        ]].copy()

        st.subheader(f"Filtered Data Table（Total: {len(df_display)} records）")
        st.dataframe(df_display.head(100))

        st.subheader("Accident Location Density Map")

        coords = df_filtered[["GPS座標X", "GPS座標Y"]].dropna()
        kde = KernelDensity(kernel='gaussian', bandwidth=0.01).fit(coords)
        df_filtered["密度"] = np.exp(kde.score_samples(coords))

        def density_to_color(value, max_density):
            ratio = value / max_density
            if ratio < 0.25:
                return [0, 255, 0]
            elif ratio < 0.5:
                return [255, 255, 0]
            elif ratio < 0.75:
                return [255, 128, 0]
            elif ratio < 0.95:
                return [255, 0, 0]
            else:
                return [128, 0, 255]

        max_density = df_filtered["密度"].max()
        df_filtered["color"] = df_filtered["密度"].apply(lambda x: density_to_color(x, max_density))

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_filtered,
            get_position='[GPS座標X, GPS座標Y]',
            get_color="color",
            get_radius=40,
            pickable=True,
            opacity=0.8,
        )

        view_state = pdk.ViewState(
            longitude=df_filtered["GPS座標X"].mean(),
            latitude=df_filtered["GPS座標Y"].mean(),
            zoom=11,
            pitch=50,
        )

        scatter_map = pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            tooltip={"text": "Accident Location"},
        )

        st.pydeck_chart(scatter_map)

        st.subheader("Casualty Trends Over Time")

        option = st.selectbox("Please select the data category to display", ("Deaths", "Injuries"))

        daily = df_filtered.groupby("日期")[["Deaths", "Injuries"]].sum().reset_index()

        if option == "Deaths":
            st.line_chart(daily.set_index("日期")[["Deaths"]])
        elif option == "Injuries":
            st.line_chart(daily.set_index("日期")[["Injuries"]])

    else:
        st.info("Please select a complete start and end date.")

except FileNotFoundError:
    st.error("File not found. Please check if the file name and path are correct.")
