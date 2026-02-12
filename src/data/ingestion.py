from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Define schemas
class OfficerReport(BaseModel):
    officer_id: str
    region: str
    incident_type: str
    timestamp: str

class CitizenReport(BaseModel):
    citizen_id: str
    region: str
    incident_type: str
    timestamp: str

# Simple DB setup (SQLite)
conn = sqlite3.connect("smart_patrol.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    region TEXT,
    incident_type TEXT,
    timestamp TEXT
)""")
conn.commit()

@app.post("/officer_reports")
def ingest_officer(report: OfficerReport):
    cursor.execute("INSERT INTO incidents (source, region, incident_type, timestamp) VALUES (?, ?, ?, ?)",
                   ("officer", report.region, report.incident_type, report.timestamp))
    conn.commit()
    return {"status": "success", "source": "officer"}

@app.post("/citizen_reports")
def ingest_citizen(report: CitizenReport):
    cursor.execute("INSERT INTO incidents (source, region, incident_type, timestamp) VALUES (?, ?, ?, ?)",
                   ("citizen", report.region, report.incident_type, report.timestamp))
    conn.commit()
    return {"status": "success", "source": "citizen"}

@app.post("/bulk_upload")
def ingest_bulk(reports: list[OfficerReport]):
    for report in reports:
        cursor.execute("INSERT INTO incidents (source, region, incident_type, timestamp) VALUES (?, ?, ?, ?)",
                       ("bulk", report.region, report.incident_type, report.timestamp))
    conn.commit()
    return {"status": "success", "count": len(reports)}
