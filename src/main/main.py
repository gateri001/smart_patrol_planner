from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import random
import joblib

app = FastAPI(title="Smart Patrol Planner")
model_data = joblib.load("model.pkl")

model = model_data["model"]
le_area = model_data["le_area"]
le_type = model_data["le_type"]
le_risk = model_data["le_risk"]

# --- AUTH SETUP ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

users_db = {
    "officer1": pwd_context.hash("securepassword")
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": username, "token_type": "bearer"}

@app.get("/secure-data")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": f"Access granted for {token}"}

# --- PREDICTION SETUP ---
class Incident(BaseModel):
    region: str
    incident_type: str
    timestamp: str

def predict_hotspot(region, incident_type, timestamp):
    hour = int(timestamp.split(" ")[1].split(":")[0])

    area_encoded = le_area.transform([region])[0]
    type_encoded = le_type.transform([incident_type])[0]

    prediction = model.predict([[area_encoded, type_encoded, hour]])

    risk_label = le_risk.inverse_transform(prediction)[0]

    return risk_label

@app.post("/predict")
def predict_hotspot_api(incident: Incident):
    risk = predict_hotspot(
        incident.region,
        incident.incident_type,
        incident.timestamp
    )

    return {
        "region": incident.region,
        "incident_type": incident.incident_type,
        "predicted_risk": risk,
        "message": f"Crime hotspot risk for {incident.region} is {risk}"
    }

@app.get("/")
def root():
    return {"message": "Smart Patrol Planner API is running"}
