import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Dataset path
dataset_path = project_folder / "dataset" / "energydata_complete.csv"

# Load dataset
data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# Remove date column
data = data.drop("date", axis=1)


# Input features
X = data.drop("Appliances", axis=1)

# Target
y = data["Appliances"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)


# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)


# Evaluate model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)


print("\nModel trained successfully!")

print("\nModel Performance")
print("-------------------------")
print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)
print("R2 Score:", r2)


# Compare actual and predicted values
result = pd.DataFrame({
    "Actual Energy": y_test.iloc[:10].values,
    "Predicted Energy": predictions[:10]
})

print("\nActual vs Predicted Energy")
print(result)