import streamlit as st
import pandas as pd
import numpy as np

from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Traffic Violations Dashboard",
    layout="wide"
)

st.title("🚔 Traffic Violations Analytics Dashboard")

# =====================================================
# DATABASE CONNECTION
# =====================================================

DB_USER = "root"
DB_PASSWORD = "Tommy*123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "traffic_violations"

engine = create_engine(
    f"mysql+pymysql://root:Tommy*123@localhost:3306/traffic_violations"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(show_spinner=True)
def load_data():

    query = """
    SELECT
        `Date Of Stop`,
        Location,
        VehicleType,
        Gender,
        Race,
        `Violation Type`,
        Accident,
        Make,
        Model,
        Latitude,
        Longitude
    FROM traffic_violations
    """

    df = pd.read_sql(query, engine)

    df["Date Of Stop"] = pd.to_datetime(
        df["Date Of Stop"],
        errors="coerce"
    )

    categorical_cols = [
        "Location",
        "VehicleType",
        "Gender",
        "Race",
        "Violation Type",
        "Accident",
        "Make",
        "Model"
    ]

    for col in categorical_cols:
        df[col] = df[col].astype("category")

    return df


df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Traffic Violations")

# Date Filter

min_date = df["Date Of Stop"].min()
max_date = df["Date Of Stop"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

# Location

locations = sorted(
    df["Location"]
    .dropna()
    .astype(str)
    .unique()
)

selected_location = st.sidebar.multiselect(
    "Location",
    locations
)

# Vehicle Type

vehicle_types = sorted(
    df["VehicleType"]
    .dropna()
    .astype(str)
    .unique()
)

selected_vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    vehicle_types
)

# Gender

genders = sorted(
    df["Gender"]
    .dropna()
    .astype(str)
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    genders
)

# Race

races = sorted(
    df["Race"]
    .dropna()
    .astype(str)
    .unique()
)

selected_race = st.sidebar.multiselect(
    "Race",
    races
)

# Violation Type

violations = sorted(
    df["Violation Type"]
    .dropna()
    .astype(str)
    .unique()
)

selected_violation = st.sidebar.multiselect(
    "Violation Category",
    violations
)

# =====================================================
# FILTER DATA
# =====================================================

mask = pd.Series(True, index=df.index)

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    mask &= (
        (df["Date Of Stop"] >= start_date)
        &
        (df["Date Of Stop"] <= end_date)
    )

if selected_location:
    mask &= df["Location"].astype(str).isin(selected_location)

if selected_vehicle:
    mask &= df["VehicleType"].astype(str).isin(selected_vehicle)

if selected_gender:
    mask &= df["Gender"].astype(str).isin(selected_gender)

if selected_race:
    mask &= df["Race"].astype(str).isin(selected_race)

if selected_violation:
    mask &= df["Violation Type"].astype(str).isin(selected_violation)

filtered_df = df.loc[mask]

# =====================================================
# SUMMARY METRICS
# =====================================================

st.header("📊 Summary Statistics")

total_violations = len(filtered_df)

accident_count = (
    filtered_df["Accident"]
    .astype(str)
    .str.upper()
    .eq("YES")
    .sum()
)

high_risk_zone = (
    filtered_df["Location"]
    .value_counts()
)

top_make = (
    filtered_df["Make"]
    .value_counts()
)

top_model = (
    filtered_df["Model"]
    .value_counts()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Violations",
    f"{total_violations:,}"
)

c2.metric(
    "Accident Violations",
    f"{accident_count:,}"
)

c3.metric(
    "High Risk Zone",
    high_risk_zone.index[0]
    if len(high_risk_zone)
    else "N/A"
)

c4.metric(
    "Top Make",
    top_make.index[0]
    if len(top_make)
    else "N/A"
)

c5.metric(
    "Top Model",
    top_model.index[0]
    if len(top_model)
    else "N/A"
)

# =====================================================
# TREND ANALYSIS (PLOTLY)
# =====================================================

st.header("📈 Violation Trend")

trend_df = (
    filtered_df
    .groupby(
        filtered_df["Date Of Stop"].dt.to_period("M")
    )
    .size()
    .reset_index(name="Violations")
)

trend_df["Date Of Stop"] = (
    trend_df["Date Of Stop"]
    .astype(str)
)

fig = px.line(
    trend_df,
    x="Date Of Stop",
    y="Violations",
    markers=True,
    title="Monthly Violation Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VIOLATION CATEGORY (PLOTLY)
# =====================================================

st.header("🚨 Violation Categories")

viol_df = (
    filtered_df["Violation Type"]
    .value_counts()
    .head(15)
    .reset_index()
)

viol_df.columns = [
    "Violation Type",
    "Count"
]

fig = px.bar(
    viol_df,
    x="Violation Type",
    y="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VEHICLE TYPES (SEABORN)
# =====================================================

st.header("🚗 Top Vehicle Types")

fig, ax = plt.subplots(figsize=(10, 6))

sns.countplot(
    data=filtered_df,
    y="VehicleType",
    order=filtered_df["VehicleType"]
    .value_counts()
    .head(10)
    .index,
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# =====================================================
# RACE DISTRIBUTION (PLOTLY PIE)
# =====================================================

st.header("👥 Race Distribution")

race_df = (
    filtered_df["Race"]
    .value_counts()
    .head(10)
    .reset_index()
)

race_df.columns = [
    "Race",
    "Count"
]

fig = px.pie(
    race_df,
    names="Race",
    values="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# GENDER DISTRIBUTION
# =====================================================

st.header("🚻 Gender Distribution")

gender_df = (
    filtered_df["Gender"]
    .value_counts()
    .reset_index()
)

gender_df.columns = [
    "Gender",
    "Count"
]

fig = px.bar(
    gender_df,
    x="Gender",
    y="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VEHICLE MAKES
# =====================================================

st.header("🏭 Top Vehicle Makes")

make_df = (
    filtered_df["Make"]
    .value_counts()
    .head(15)
    .reset_index()
)

make_df.columns = [
    "Make",
    "Count"
]

fig = px.bar(
    make_df,
    x="Make",
    y="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VEHICLE MODELS
# =====================================================

st.header("🚘 Top Vehicle Models")

model_df = (
    filtered_df["Model"]
    .value_counts()
    .head(15)
    .reset_index()
)

model_df.columns = [
    "Model",
    "Count"
]

fig = px.bar(
    model_df,
    x="Model",
    y="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.header("🗺 Incident Hotspots")

heat_df = filtered_df[
    ["Latitude", "Longitude"]
].dropna()

if len(heat_df) > 10000:

    heat_df = heat_df.sample(
        10000,
        random_state=42
    )

if len(heat_df):

    m = folium.Map(
        location=[
            heat_df["Latitude"].mean(),
            heat_df["Longitude"].mean()
        ],
        zoom_start=10
    )

    HeatMap(
        heat_df.values.tolist(),
        radius=8
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=600
    )

# =====================================================
# HIGH RISK ZONES
# =====================================================

st.header("🔥 High Risk Zones")

risk_df = (
    filtered_df["Location"]
    .value_counts()
    .head(15)
    .reset_index()
)

risk_df.columns = [
    "Location",
    "Violations"
]

fig = px.bar(
    risk_df,
    x="Violations",
    y="Location",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# RAW DATA (PAGINATION)
# =====================================================

st.header("📄 Filtered Records")

page_size = 100

page = st.number_input(
    "Page Number",
    min_value=1,
    value=1
)

start = (page - 1) * page_size
end = start + page_size

st.write(
    f"Showing {start:,} to {min(end,len(filtered_df)):,} "
    f"of {len(filtered_df):,} rows"
)

st.dataframe(
    filtered_df.iloc[start:end],
    use_container_width=True
)