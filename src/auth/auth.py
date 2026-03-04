from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI(title="Smart Patrol Auth Service")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Demo user database
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
