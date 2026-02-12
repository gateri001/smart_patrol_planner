from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user store
users_db = {
    "officer1": pwd_context.hash("securepassword")
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/token")
def login(username: str, password: str):
    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": username, "token_type": "bearer"}

@app.get("/secure-data")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": f"Access granted for {token}"}
