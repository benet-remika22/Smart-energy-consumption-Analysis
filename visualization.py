import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "dataset" / "energydata_complete.csv"

# Load dataset
data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", data.shape)

# Convert date column
data["date"] = pd.to_datetime(data["date"])

# -------------------------------
# Graph 1: Energy Consumption
# -------------------------------

plt.figure(figsize=(10, 5))

plt.plot(data["date"], data["Appliances"])

plt.xlabel("Date")
plt.ylabel("Energy Consumption")
plt.title("Energy Consumption Over Time")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# -------------------------------
# Graph 2: Energy Distribution
# -------------------------------

plt.figure(figsize=(8, 5))

plt.hist(data["Appliances"], bins=30)

plt.xlabel("Energy Consumption")
plt.ylabel("Frequency")
plt.title("Energy Consumption Distribution")

plt.tight_layout()

plt.show()