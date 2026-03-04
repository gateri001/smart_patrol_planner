import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("../../datasets/sample_incidents.csv")

# --- Create Risk Label from Severity ---
def severity_to_risk(severity):
    if severity <= 2:
        return "Low"
    elif severity == 3:
        return "Medium"
    else:
        return "High"

df["risk"] = df["severity"].apply(severity_to_risk)

# --- Feature Engineering ---
# Extract hour from time
df["hour"] = df["time"].str.split(":").str[0].astype(int)

# Select features
X = df[["area", "type", "hour"]]
y = df["risk"]

# Encode categorical variables
le_area = LabelEncoder()
le_type = LabelEncoder()
le_risk = LabelEncoder()

X["area"] = le_area.fit_transform(X["area"])
X["type"] = le_type.fit_transform(X["type"])
y = le_risk.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save everything needed for inference
joblib.dump({
    "model": model,
    "le_area": le_area,
    "le_type": le_type,
    "le_risk": le_risk
}, "model.pkl")

print("Model trained and saved as model.pkl")
