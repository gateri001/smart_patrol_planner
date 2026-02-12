from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Input schema
class Incident(BaseModel):
    region: str
    incident_type: str
    timestamp: str

# Dummy hotspot prediction logic
def predict_hotspot(region: str):
    # Placeholder: randomly assign risk level
    risk_levels = ["Low", "Medium", "High"]
    return random.choice(risk_levels)

@app.post("/predict")
def predict_hotspot_api(incident: Incident):
    risk = predict_hotspot(incident.region)
    return {
        "region": incident.region,
        "incident_type": incident.incident_type,
        "predicted_risk":
