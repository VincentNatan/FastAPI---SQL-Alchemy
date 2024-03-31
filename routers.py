from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal
from typing import List, Any, Dict
from sqlalchemy.exc import IntegrityError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(**user.dict())
        return crud.create_user(db, db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.get("/user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[schemas.User])
def get_users_Pagination(skip: int = 0, limit: int = 10, sort_by: str = None, db: Session = Depends(get_db)):
    if sort_by not in ["id", "name", "email"]:
        sort_by = "id" 

    users = crud.get_users(db, skip=skip, limit=limit, sort_by=sort_by)
    return users

@router.put("/update/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: Dict[str, Any], db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        updated_user = crud.update_user(db, user_id, user)
        return updated_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    return {"message": "User deleted successfully"}
