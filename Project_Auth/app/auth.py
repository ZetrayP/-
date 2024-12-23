import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from .models import User, LoginHistory, TokenBlacklist
from .schemas import UserCreate, UserUpdate, UserOut
from .database import get_session

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")    
    try:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        session.add(db_user)
        session.commit()
        access_token = create_access_token(data={"sub": db_user.email})
        return {"detail": "Registration successful", "access_token": access_token}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")   
    login_history = LoginHistory(user_id=db_user.id, user_agent="User-Agent Info")
    session.add(login_history)
    session.commit() 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    return {"detail": "Login successful", "access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh")
def refresh_token(refresh_token: str, session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_blacklist = TokenBlacklist(token=refresh_token)
        session.add(token_blacklist)
        session.commit()
    except JWTError:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
    return {"detail": "Token refreshed successfully", "access_token": new_access_token}

@router.put("/user/update", response_model=UserOut)
def update_user(user: UserUpdate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password:
        db_user.hashed_password = pwd_context.hash(user.password)
    session.commit()
    return {"detail": "User data updated successfully", "user": db_user}

@router.get("/user/history")
def get_login_history(user_id: int, session: Session = Depends(get_session)):
    statement = select(LoginHistory).where(LoginHistory.user_id == user_id)
    history = session.exec(statement).all()
    return {"detail": "Login history retrieved successfully", "history": history}

@router.post("/logout")
def logout(refresh_token: str, session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    token_blacklist = TokenBlacklist(token=refresh_token)
    session.add(token_blacklist)
    session.commit()
    return {"detail": "User logged out successfully"}
