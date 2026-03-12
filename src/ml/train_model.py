import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("../../datasets/kenya_emergencies.csv")

# Extract hour from time
df["hour"] = df["time"].str.split(":").str[0].astype(int)

# Encoders
le_area = LabelEncoder()
le_type = LabelEncoder()
le_severity = LabelEncoder()

df["area_encoded"] = le_area.fit_transform(df["area"])
df["type_encoded"] = le_type.fit_transform(df["type"])
df["severity_encoded"] = le_severity.fit_transform(df["severity"])

# Features
X = df[["area_encoded", "type_encoded", "hour"]]

# Target
y = df["severity_encoded"]

# Train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X, y)

# Save model
joblib.dump({
    "model": model,
    "le_area": le_area,
    "le_type": le_type,
    "le_risk": le_severity
}, "../../src/main/model.pkl")

print("Model trained successfully")
