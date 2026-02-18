from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    # Convert Pydantic schema to SQLAlchemy model
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = User(email=user.email, password=user.password)
    new_user = user_repo.add_user(db_user)
    return new_user


@router.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    users = user_repo.get_all_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user