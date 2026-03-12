from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import joblib

# -------------------------
# APP SETUP
# -------------------------

app = FastAPI(title="Smart Patrol Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# LOAD AI MODEL
# -------------------------

model_data = joblib.load("model.pkl")

model = model_data["model"]
le_area = model_data["le_area"]
le_type = model_data["le_type"]
le_risk = model_data["le_risk"]

print("Known Areas:", le_area.classes_)
print("Known Types:", le_type.classes_)

# -------------------------
# AUTHENTICATION
# -------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

users_db = {
    "officer1": pwd_context.hash("securepassword")
}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

emergency_reports = []

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    username = form_data.username
    password = form_data.password

    if username not in users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, users_db[username]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "access_token": username,
        "token_type": "bearer"
    }


@app.get("/secure-data")
def secure_endpoint(token: str = Depends(oauth2_scheme)):

    return {"message": f"Access granted for {token}"}

# -------------------------
# AI PREDICTION
# -------------------------

class Incident(BaseModel):
    region: str
    incident_type: str
    timestamp: str


def predict_hotspot(region, incident_type, timestamp):

    region = region.strip()

    if region.lower() == "cbd":
        region = "CBD"
    else:
        region = region.title()
    incident_type = incident_type.strip().lower()

    try:
        hour = int(timestamp.split(" ")[1].split(":")[0])
    except:
        hour = 12  # fallback if time missing

    try:
        area_encoded = le_area.transform([region])[0]
        type_encoded = le_type.transform([incident_type])[0]
    except:
        return "Unknown"

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
        "message": f"Predicted {incident.incident_type} risk in {incident.region} is {risk}"
    }

# -------------------------
# EMERGENCY REPORTING
# -------------------------

class EmergencyReport(BaseModel):
    type: str
    area: str
    description: str
    timestamp: str


@app.post("/report-emergency")
def report_emergency(report: EmergencyReport):

    emergency_type = report.type.strip().lower()
    area = report.area.strip().title()

    # Unified warning message
    alert = f"⚠️ Unconfirmed {emergency_type} warning at {area}. Exercise caution and move to safety."

    report_data = {
        "alert": alert,
        "type": emergency_type,
        "area": area,
        "description": report.description,
        "timestamp": report.timestamp
    }

    emergency_reports.append(report_data)

    return report_data

@app.get("/emergencies")
def get_emergencies():
    return emergency_reports
# -------------------------
# ROOT ENDPOINT
# -------------------------

@app.get("/")
def root():
    return {"message": "Smart Patrol Planner API is running"}
