from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import SessionLocal, Base, engine
from models import User
from auth import hash_password, verify_password, create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS setup – make sure it's AFTER the FastAPI() init and BEFORE routes
origins = [
    "https://kzmgzrkje4v8sw6d91ko.lite.vusercontent.net",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB setup
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Header
from auth import decode_token

@app.get("/me")
def get_me(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    return {
        "email": payload.get("sub"),
        "name": payload.get("name")
    }

# ✅ Models
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class SigninRequest(BaseModel):
    name: str
    email: str
    password: str

# ✅ Routes
@app.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_pw = hash_password(payload.password)
    new_user = User(
    name=payload.name,
    email=payload.email,
    hashed_password=hashed_pw
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "name": new_user.name})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/signin")
def signin(payload: SigninRequest, db: Session = Depends(get_db)):
    print(f"Signin attempt for: {payload.email}")
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        print("Signin failed")
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    print("Signin successful")
    token = create_access_token({"sub": user.email, "name": user.name})
    return {"access_token": token, "token_type": "bearer"}

class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None

