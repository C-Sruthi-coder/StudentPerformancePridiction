import pandas as pd
import numpy as np

# Load student dataset
df = pd.read_csv("student_performance.csv")

# Input features
features = [
    "Python",
    "Java",
    "DBMS",
    "OS",
    "DMS",
    "Python_Att",
    "Java_Att",
    "DBMS_Att",
    "OS_Att",
    "DMS_Att"
]

# Create FinalMarks for the demo dataset
np.random.seed(42)

study_average = df[
    ["Python", "Java", "DBMS", "OS", "DMS"]
].mean(axis=1)

attendance_average = df[
    ["Python_Att", "Java_Att", "DBMS_Att", "OS_Att", "DMS_Att"]
].mean(axis=1)

noise = np.random.normal(0, 2, len(df))

df["FinalMarks"] = (
    study_average * 0.75
    + attendance_average * 0.25
    + noise
)

# Keep marks between 0 and 100
df["FinalMarks"] = df["FinalMarks"].clip(0, 100)

# Input data
X = df[features].values

# Target data
y = df["FinalMarks"].values

# Add bias/intercept column
X_with_bias = np.column_stack((np.ones(len(X)), X))

# Multiple Linear Regression using NumPy
coefficients = np.linalg.lstsq(
    X_with_bias,
    y,
    rcond=None
)[0]

# Predictions
predictions = X_with_bias @ coefficients

# Calculate Mean Absolute Error
mae = np.mean(np.abs(y - predictions))

print("Model trained successfully.")
print()
print("Number of students:", len(df))
print("Mean Absolute Error:", round(mae, 2))

print()
print("Model coefficients:")
print(coefficients)

# Save updated dataset
df.to_csv("student_performance.csv", index=False)

print()
print("FinalMarks column added to student_performance.csv")