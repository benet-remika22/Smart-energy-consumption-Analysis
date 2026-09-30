# ============================================================
# SMART ENERGY CONSUMPTION ANALYTICS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
file_name ="dataset/smart_energy_consumption_peak_load_analysis.csv (1).xls"
df = pd.read_csv(file_name)
print("\n============================================")
print("     SMART ENERGY CONSUMPTION ANALYTICS")
print("============================================")
print("\nDataset loaded successfully!")
print("\n----- FIRST 5 RECORDS -----")
print(df.head())
print("\n----- DATASET SHAPE -----")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n----- COLUMN NAMES -----")
print(df.columns.tolist())

print("\n----- DATA TYPES -----")
print(df.dtypes)

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())

print("\n----- DUPLICATE RECORDS -----")
print(df.duplicated().sum())




df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

print("\n----- CLEANED COLUMN NAMES -----")
print(df.columns.tolist())


if "date_time" in df.columns:

    df["date_time"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    # Extract date and time information
    df["date"] = df["date_time"].dt.date
    df["hour"] = df["date_time"].dt.hour
    df["day"] = df["date_time"].dt.day_name()
    df["month"] = df["date_time"].dt.month_name()



df = df.drop_duplicates()

print("\nDuplicate records removed.")




numeric_columns = df.select_dtypes(
    include=np.number
).columns

for column in numeric_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )

print("\nMissing numerical values handled.")




energy_column = "energy_consumption_kwh"

if energy_column in df.columns:

    total_energy = df[energy_column].sum()

    average_energy = df[energy_column].mean()

    maximum_energy = df[energy_column].max()

    minimum_energy = df[energy_column].min()

    std_energy = df[energy_column].std()

else:

    total_energy = 0
    average_energy = 0
    maximum_energy = 0
    minimum_energy = 0
    std_energy = 0


print("\n============================================")
print("       ENERGY CONSUMPTION STATISTICS")
print("============================================")

print(
    f"Total Energy Consumption : "
    f"{total_energy:.2f} kWh"
)

print(
    f"Average Energy Consumption : "
    f"{average_energy:.2f} kWh"
)

print(
    f"Maximum Energy Consumption : "
    f"{maximum_energy:.2f} kWh"
)

print(
    f"Minimum Energy Consumption : "
    f"{minimum_energy:.2f} kWh"
)

print(
    f"Standard Deviation : "
    f"{std_energy:.2f}"
)




if "building_type" in df.columns:

    building_energy = df.groupby(
        "building_type"
    )[energy_column].mean()

    print("\n============================================")
    print("   ENERGY BY BUILDING TYPE")
    print("============================================")

    print(building_energy)

    # Bar Chart
    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=building_energy.index,
        y=building_energy.values
    )

    plt.title(
        "Average Energy Consumption by Building Type"
    )

    plt.xlabel("Building Type")

    plt.ylabel(
        "Average Energy Consumption (kWh)"
    )

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.show()


if "city_zone" in df.columns:

    zone_energy = df.groupby(
        "city_zone"
    )[energy_column].mean()

    print("\n============================================")
    print("   ENERGY BY CITY ZONE")
    print("============================================")

    print(zone_energy)

    # Bar Chart
    plt.figure(figsize=(10, 5))

    sns.barplot(
        x=zone_energy.index,
        y=zone_energy.values
    )

    plt.title(
        "Average Energy Consumption by City Zone"
    )

    plt.xlabel("City Zone")

    plt.ylabel(
        "Average Energy Consumption (kWh)"
    )

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.show()



plt.figure(figsize=(9, 5))

sns.histplot(
    df[energy_column],
    bins=20,
    kde=True
)

plt.title(
    "Energy Consumption Distribution"
)

plt.xlabel(
    "Energy Consumption (kWh)"
)

plt.ylabel("Frequency")

plt.tight_layout()

plt.show()




temperature_column = "temperature_celsius"

if temperature_column in df.columns:

    temperature_correlation = df[
        temperature_column
    ].corr(
        df[energy_column]
    )

    print("\n============================================")
    print("       TEMPERATURE ANALYSIS")
    print("============================================")

    print(
        "Temperature-Energy Correlation:",
        round(temperature_correlation, 2)
    )

    # Scatter Plot
    plt.figure(figsize=(9, 5))

    sns.scatterplot(
        data=df,
        x=temperature_column,
        y=energy_column
    )

    plt.title(
        "Temperature vs Energy Consumption"
    )

    plt.xlabel(
        "Temperature (°C)"
    )

    plt.ylabel(
        "Energy Consumption (kWh)"
    )

    plt.tight_layout()

    plt.show()




occupancy_column = "occupancy_level"

if occupancy_column in df.columns:

    occupancy_correlation = df[
        occupancy_column
    ].corr(
        df[energy_column]
    )

    print("\n============================================")
    print("        OCCUPANCY ANALYSIS")
    print("============================================")

    print(
        "Occupancy-Energy Correlation:",
        round(occupancy_correlation, 2)
    )

    # Scatter Plot
    plt.figure(figsize=(9, 5))

    sns.scatterplot(
        data=df,
        x=occupancy_column,
        y=energy_column
    )

    plt.title(
        "Occupancy Level vs Energy Consumption"
    )

    plt.xlabel(
        "Occupancy Level"
    )

    plt.ylabel(
        "Energy Consumption (kWh)"
    )

    plt.tight_layout()

    plt.show()




if "peak_hour" in df.columns:

    peak_energy = df.groupby(
        "peak_hour"
    )[energy_column].mean()

    print("\n============================================")
    print("          PEAK HOUR ANALYSIS")
    print("============================================")

    print(peak_energy)

    # Bar Chart
    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=peak_energy.index,
        y=peak_energy.values
    )

    plt.title(
        "Average Energy Consumption by Peak Hour"
    )

    plt.xlabel("Peak Hour")

    plt.ylabel(
        "Average Energy Consumption (kWh)"
    )

    plt.tight_layout()

    plt.show()




renewable_column = (
    "renewable_energy_used_percentage"
)

# IMPORTANT:
# Calculate renewable_average BEFORE final summary

if renewable_column in df.columns:

    renewable_average = df[
        renewable_column
    ].mean()

else:

    renewable_average = 0


print("\n============================================")
print("       RENEWABLE ENERGY ANALYSIS")
print("============================================")

print(
    f"Average Renewable Energy Used : "
    f"{renewable_average:.2f}%"
)




if (
    renewable_column in df.columns
    and "building_type" in df.columns
):

    renewable_building = df.groupby(
        "building_type"
    )[renewable_column].mean()

    print("\nRenewable Energy by Building Type:")

    print(renewable_building)

    # Bar Chart
    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=renewable_building.index,
        y=renewable_building.values
    )

    plt.title(
        "Renewable Energy Usage by Building Type"
    )

    plt.xlabel("Building Type")

    plt.ylabel(
        "Renewable Energy Used (%)"
    )

    plt.tight_layout()

    plt.show()




risk_column = "peak_load_risk"

if risk_column in df.columns:

    risk_counts = df[
        risk_column
    ].value_counts()

    print("\n============================================")
    print("        PEAK LOAD RISK ANALYSIS")
    print("============================================")

    print(risk_counts)

    # Count Plot
    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x=risk_column
    )

    plt.title(
        "Peak Load Risk Distribution"
    )

    plt.xlabel(
        "Peak Load Risk"
    )

    plt.ylabel(
        "Number of Records"
    )

    plt.tight_layout()

    plt.show()




if (
    "building_type" in df.columns
    and "peak_load_risk" in df.columns
):

    risk_table = pd.crosstab(
        df["building_type"],
        df["peak_load_risk"]
    )

    print("\n============================================")
    print("     BUILDING TYPE VS PEAK LOAD RISK")
    print("============================================")

    print(risk_table)

    # Grouped Bar Chart
    risk_table.plot(
        kind="bar",
        figsize=(10, 6)
    )

    plt.title(
        "Peak Load Risk by Building Type"
    )

    plt.xlabel(
        "Building Type"
    )

    plt.ylabel(
        "Number of Records"
    )

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.show()



numeric_df = df.select_dtypes(
    include=np.number
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title(
    "Correlation Heatmap of Energy Factors"
)

plt.tight_layout()

plt.show()



highest_record = df.loc[
    df[energy_column].idxmax()
]

print("\n============================================")
print("    HIGHEST ENERGY CONSUMPTION RECORD")
print("============================================")

print(highest_record)




lowest_record = df.loc[
    df[energy_column].idxmin()
]

print("\n============================================")
print("     LOWEST ENERGY CONSUMPTION RECORD")
print("============================================")

print(lowest_record)




mean_energy = df[
    energy_column
].mean()

std_energy = df[
    energy_column
].std()

# NumPy used to calculate threshold
threshold = mean_energy + std_energy

df["consumption_level"] = np.where(
    df[energy_column] > threshold,
    "High",
    "Normal"
)


print("\n============================================")
print("     HIGH ENERGY CONSUMPTION DETECTION")
print("============================================")

print(
    df["consumption_level"].value_counts()
)




high_consumption = df[
    df["consumption_level"] == "High"
]

print("\n----- HIGH CONSUMPTION RECORDS -----")

print(
    high_consumption[
        [
            energy_column,
            "consumption_level"
        ]
    ].head(10)
)




if "date_time" in df.columns:

    fig = px.line(
        df,
        x="date_time",
        y=energy_column,
        title="Interactive Energy Consumption Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date-Time",
        yaxis_title="Energy Consumption (kWh)"
    )

    fig.show()




if "building_type" in df.columns:

    building_plot = df.groupby(
        "building_type",
        as_index=False
    )[energy_column].mean()

    fig = px.bar(
        building_plot,
        x="building_type",
        y=energy_column,
        title="Average Energy Consumption by Building Type"
    )

    fig.show()




if (
    temperature_column in df.columns
    and "building_type" in df.columns
):

    fig = px.scatter(
        df,
        x=temperature_column,
        y=energy_column,
        color="building_type",
        title="Temperature vs Energy Consumption"
    )

    fig.show()




if "city_zone" in df.columns:

    zone_plot = df.groupby(
        "city_zone",
        as_index=False
    )[energy_column].mean()

    fig = px.bar(
        zone_plot,
        x="city_zone",
        y=energy_column,
        title="Average Energy Consumption by City Zone"
    )

    fig.show()




print("\n")
print("============================================")
print("       SMART ENERGY ANALYTICS SUMMARY")
print("============================================")

print(
    f"Total Energy Consumption : "
    f"{total_energy:.2f} kWh"
)

print(
    f"Average Energy Consumption : "
    f"{average_energy:.2f} kWh"
)

print(
    f"Maximum Energy Consumption : "
    f"{maximum_energy:.2f} kWh"
)

print(
    f"Minimum Energy Consumption : "
    f"{minimum_energy:.2f} kWh"
)

print(
    f"High Consumption Records : "
    f"{len(high_consumption)}"
)

print(
    f"Average Renewable Energy : "
    f"{renewable_average:.2f}%"
)

print("============================================")

print(
    "\nSmart Energy Consumption Analysis "
    "Completed Successfully!"
)

print("============================================")