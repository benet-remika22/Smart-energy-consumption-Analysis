import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "dataset" / "energydata_complete.csv"

# Load dataset
data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", data.shape)

# Select numerical columns
numeric_data = data.select_dtypes(include="number")

# Calculate correlation
correlation = numeric_data.corr()

# Display correlation with Appliances
print("\nCorrelation with Appliances:")
print(correlation["Appliances"].sort_values(ascending=False))

# Create bar chart
correlation["Appliances"].sort_values(ascending=False).head(10).plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Top Factors Affecting Energy Consumption")
plt.xlabel("Features")
plt.ylabel("Correlation")

plt.tight_layout()
plt.show()