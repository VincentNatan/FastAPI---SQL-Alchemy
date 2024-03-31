from sqlalchemy.orm import Session
import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10, sort_by: str = "id"):
    if sort_by == "id":
        return db.query(models.User).offset(skip).limit(limit).all()
    else:
        return db.query(models.User).order_by(getattr(models.User, sort_by)).offset(skip).limit(limit).all()

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_data: dict):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()

