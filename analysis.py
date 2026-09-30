import pandas as pd

# Load dataset
data = pd.read_csv("../dataset/energydata_complete.csv")

print("Dataset loaded successfully!")
print("Shape:", data.shape)

# First 5 rows
print("\nFirst 5 rows:")
print(data.head())

# Column names
print("\nColumns:")
print(data.columns)

# Missing values
print("\nMissing values:")
print(data.isnull().sum())

# Basic statistics
print("\nBasic Statistics:")
print(data.describe())