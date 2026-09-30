
# ============================================================
# SMART ENERGY CONSUMPTION ANALYTICS - STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Energy Analytics",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("⚡ Smart Energy Consumption Analytics Dashboard")
st.markdown(
    "Interactive dashboard for analyzing energy consumption, "
    "building types, temperature, occupancy, renewable energy "
    "and peak load risk."
)

st.divider()


# ============================================================
# LOAD DATASET
# ============================================================

file_name = "dataset/smart_energy_consumption_peak_load_analysis.csv (1).xls"

try:

    # Try reading as CSV first
    df = pd.read_csv(file_name)

except Exception:

    try:
        # If the file is actually an Excel file
        df = pd.read_excel(file_name)

    except Exception as e:

        st.error("Unable to load the dataset.")
        st.write(e)
        st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)


# ============================================================
# DATE AND TIME PROCESSING
# ============================================================

if "date_time" in df.columns:

    df["date_time"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    df["date"] = df["date_time"].dt.date
    df["hour"] = df["date_time"].dt.hour
    df["day"] = df["date_time"].dt.day_name()
    df["month"] = df["date_time"].dt.month_name()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates()


# ============================================================
# HANDLE MISSING NUMERICAL VALUES
# ============================================================

numeric_columns = df.select_dtypes(
    include=np.number
).columns

for column in numeric_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )


# ============================================================
# COLUMN NAMES
# ============================================================

energy_column = "energy_consumption_kwh"
temperature_column = "temperature_celsius"
occupancy_column = "occupancy_level"
renewable_column = "renewable_energy_used_percentage"
risk_column = "peak_load_risk"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()


# ------------------------------------------------------------
# Building Type Filter
# ------------------------------------------------------------

if "building_type" in df.columns:

    building_options = sorted(
        df["building_type"].dropna().unique().tolist()
    )

    selected_buildings = st.sidebar.multiselect(
        "Building Type",
        building_options,
        default=building_options
    )

    filtered_df = filtered_df[
        filtered_df["building_type"].isin(
            selected_buildings
        )
    ]


# ------------------------------------------------------------
# City Zone Filter
# ------------------------------------------------------------

if "city_zone" in df.columns:

    zone_options = sorted(
        df["city_zone"].dropna().unique().tolist()
    )

    selected_zones = st.sidebar.multiselect(
        "City Zone",
        zone_options,
        default=zone_options
    )

    filtered_df = filtered_df[
        filtered_df["city_zone"].isin(
            selected_zones
        )
    ]


# ------------------------------------------------------------
# Peak Load Risk Filter
# ------------------------------------------------------------

if risk_column in df.columns:

    risk_options = sorted(
        df[risk_column].dropna().unique().tolist()
    )

    selected_risk = st.sidebar.multiselect(
        "Peak Load Risk",
        risk_options,
        default=risk_options
    )

    filtered_df = filtered_df[
        filtered_df[risk_column].isin(
            selected_risk
        )
    ]


# ============================================================
# ENERGY CALCULATIONS
# ============================================================

if energy_column in filtered_df.columns:

    total_energy = filtered_df[
        energy_column
    ].sum()

    average_energy = filtered_df[
        energy_column
    ].mean()

    maximum_energy = filtered_df[
        energy_column
    ].max()

    minimum_energy = filtered_df[
        energy_column
    ].min()

    std_energy = filtered_df[
        energy_column
    ].std()

else:

    total_energy = 0
    average_energy = 0
    maximum_energy = 0
    minimum_energy = 0
    std_energy = 0


# ============================================================
# RENEWABLE ENERGY
# ============================================================

if renewable_column in filtered_df.columns:

    renewable_average = filtered_df[
        renewable_column
    ].mean()

else:

    renewable_average = 0


# ============================================================
# HIGH CONSUMPTION DETECTION
# ============================================================

if energy_column in filtered_df.columns:

    mean_energy = filtered_df[
        energy_column
    ].mean()

    std_energy = filtered_df[
        energy_column
    ].std()

    threshold = mean_energy + std_energy

    filtered_df["consumption_level"] = np.where(
        filtered_df[energy_column] > threshold,
        "High",
        "Normal"
    )

    high_consumption = filtered_df[
        filtered_df["consumption_level"] == "High"
    ]

else:

    high_consumption = pd.DataFrame()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Energy Consumption Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Energy",
        f"{total_energy:.2f} kWh"
    )

with col2:
    st.metric(
        "Average Energy",
        f"{average_energy:.2f} kWh"
    )

with col3:
    st.metric(
        "Maximum Energy",
        f"{maximum_energy:.2f} kWh"
    )

with col4:
    st.metric(
        "Minimum Energy",
        f"{minimum_energy:.2f} kWh"
    )

with col5:
    st.metric(
        "High Consumption",
        len(high_consumption)
    )


st.divider()


# ============================================================
# SECOND KPI ROW
# ============================================================

col6, col7, col8 = st.columns(3)

with col6:

    st.metric(
        "Renewable Energy",
        f"{renewable_average:.2f}%"
    )

with col7:

    st.metric(
        "Dataset Records",
        len(filtered_df)
    )

with col8:

    st.metric(
        "Dataset Columns",
        len(filtered_df.columns)
    )


st.divider()


# ============================================================
# ENERGY CONSUMPTION OVER TIME
# ============================================================

if (
    "date_time" in filtered_df.columns
    and energy_column in filtered_df.columns
):

    st.subheader("📈 Energy Consumption Over Time")

    fig = px.line(
        filtered_df,
        x="date_time",
        y=energy_column,
        title="Energy Consumption Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date and Time",
        yaxis_title="Energy Consumption (kWh)",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# BUILDING TYPE + CITY ZONE
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Building Type
# ------------------------------------------------------------

with col1:

    if (
        "building_type" in filtered_df.columns
        and energy_column in filtered_df.columns
    ):

        building_plot = filtered_df.groupby(
            "building_type",
            as_index=False
        )[energy_column].mean()

        fig = px.bar(
            building_plot,
            x="building_type",
            y=energy_column,
            title="Average Energy by Building Type",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="Building Type",
            yaxis_title="Average Energy (kWh)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# City Zone
# ------------------------------------------------------------

with col2:

    if (
        "city_zone" in filtered_df.columns
        and energy_column in filtered_df.columns
    ):

        zone_plot = filtered_df.groupby(
            "city_zone",
            as_index=False
        )[energy_column].mean()

        fig = px.bar(
            zone_plot,
            x="city_zone",
            y=energy_column,
            title="Average Energy by City Zone",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="City Zone",
            yaxis_title="Average Energy (kWh)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TEMPERATURE + OCCUPANCY ANALYSIS
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Temperature vs Energy
# ------------------------------------------------------------

with col1:

    if (
        temperature_column in filtered_df.columns
        and energy_column in filtered_df.columns
    ):

        temperature_correlation = filtered_df[
            temperature_column
        ].corr(
            filtered_df[energy_column]
        )

        st.subheader("🌡️ Temperature Analysis")

        st.metric(
            "Temperature-Energy Correlation",
            f"{temperature_correlation:.2f}"
        )

        fig = px.scatter(
            filtered_df,
            x=temperature_column,
            y=energy_column,
            color="building_type"
            if "building_type" in filtered_df.columns
            else None,
            title="Temperature vs Energy Consumption"
        )

        fig.update_layout(
            xaxis_title="Temperature (°C)",
            yaxis_title="Energy Consumption (kWh)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# Occupancy vs Energy
# ------------------------------------------------------------

with col2:

    if (
        occupancy_column in filtered_df.columns
        and energy_column in filtered_df.columns
    ):

        occupancy_correlation = filtered_df[
            occupancy_column
        ].corr(
            filtered_df[energy_column]
        )

        st.subheader("👥 Occupancy Analysis")

        st.metric(
            "Occupancy-Energy Correlation",
            f"{occupancy_correlation:.2f}"
        )

        fig = px.scatter(
            filtered_df,
            x=occupancy_column,
            y=energy_column,
            color="building_type"
            if "building_type" in filtered_df.columns
            else None,
            title="Occupancy vs Energy Consumption"
        )

        fig.update_layout(
            xaxis_title="Occupancy Level",
            yaxis_title="Energy Consumption (kWh)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PEAK HOUR + RENEWABLE ENERGY
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Peak Hour
# ------------------------------------------------------------

with col1:

    if (
        "peak_hour" in filtered_df.columns
        and energy_column in filtered_df.columns
    ):

        peak_energy = filtered_df.groupby(
            "peak_hour",
            as_index=False
        )[energy_column].mean()

        fig = px.bar(
            peak_energy,
            x="peak_hour",
            y=energy_column,
            title="Average Energy Consumption by Peak Hour",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="Peak Hour",
            yaxis_title="Average Energy (kWh)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# Renewable Energy by Building
# ------------------------------------------------------------

with col2:

    if (
        renewable_column in filtered_df.columns
        and "building_type" in filtered_df.columns
    ):

        renewable_building = filtered_df.groupby(
            "building_type",
            as_index=False
        )[renewable_column].mean()

        fig = px.bar(
            renewable_building,
            x="building_type",
            y=renewable_column,
            title="Renewable Energy Usage by Building",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="Building Type",
            yaxis_title="Renewable Energy (%)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PEAK LOAD RISK
# ============================================================

st.subheader("🚨 Peak Load Risk Analysis")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Risk Distribution
# ------------------------------------------------------------

with col1:

    if risk_column in filtered_df.columns:

        risk_counts = (
            filtered_df[risk_column]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "risk",
            "count"
        ]

        fig = px.bar(
            risk_counts,
            x="risk",
            y="count",
            title="Peak Load Risk Distribution",
            text_auto=True
        )

        fig.update_layout(
            xaxis_title="Peak Load Risk",
            yaxis_title="Number of Records",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# Building Type vs Risk
# ------------------------------------------------------------

with col2:

    if (
        "building_type" in filtered_df.columns
        and risk_column in filtered_df.columns
    ):

        risk_table = pd.crosstab(
            filtered_df["building_type"],
            filtered_df[risk_column]
        )

        risk_plot = (
            risk_table
            .reset_index()
            .melt(
                id_vars="building_type",
                var_name="risk",
                value_name="count"
            )
        )

        fig = px.bar(
            risk_plot,
            x="building_type",
            y="count",
            color="risk",
            barmode="group",
            title="Peak Load Risk by Building Type"
        )

        fig.update_layout(
            xaxis_title="Building Type",
            yaxis_title="Number of Records",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(
    include=np.number
)

if numeric_df.shape[1] > 1:

    correlation_matrix = numeric_df.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Between Energy Factors"
    )

    fig.update_layout(
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ENERGY DISTRIBUTION
# ============================================================

if energy_column in filtered_df.columns:

    st.subheader("📊 Energy Consumption Distribution")

    fig = px.histogram(
        filtered_df,
        x=energy_column,
        nbins=20,
        marginal="box",
        title="Energy Consumption Distribution"
    )

    fig.update_layout(
        xaxis_title="Energy Consumption (kWh)",
        yaxis_title="Frequency",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# HIGHEST AND LOWEST ENERGY RECORD
# ============================================================

st.subheader("⚡ Energy Consumption Extremes")

col1, col2 = st.columns(2)


with col1:

    if energy_column in filtered_df.columns:

        highest_record = filtered_df.loc[
            filtered_df[energy_column].idxmax()
        ]

        st.write("### 🔴 Highest Consumption")

        st.dataframe(
            highest_record.to_frame(
                "Value"
            ),
            use_container_width=True
        )


with col2:

    if energy_column in filtered_df.columns:

        lowest_record = filtered_df.loc[
            filtered_df[energy_column].idxmin()
        ]

        st.write("### 🟢 Lowest Consumption")

        st.dataframe(
            lowest_record.to_frame(
                "Value"
            ),
            use_container_width=True
        )


# ============================================================
# HIGH CONSUMPTION RECORDS
# ============================================================

st.subheader("🔥 High Energy Consumption Records")

if not high_consumption.empty:

    columns_to_show = [
        col
        for col in [
            "date_time",
            "building_type",
            "city_zone",
            energy_column,
            "temperature_celsius",
            "occupancy_level",
            "consumption_level"
        ]
        if col in high_consumption.columns
    ]

    st.dataframe(
        high_consumption[
            columns_to_show
        ].head(10),
        use_container_width=True
    )

else:

    st.info(
        "No high consumption records found."
    )


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)


# ============================================================
# DATASET INFORMATION
# ============================================================

with st.expander("ℹ️ Dataset Information"):

    col1, col2 = st.columns(2)

    with col1:

        st.write("### Shape")

        st.write(
            f"Rows: {filtered_df.shape[0]}"
        )

        st.write(
            f"Columns: {filtered_df.shape[1]}"
        )

    with col2:

        st.write("### Column Names")

        st.write(
            filtered_df.columns.tolist()
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.success(
    "✅ Smart Energy Consumption Analysis Completed Successfully!"
)
