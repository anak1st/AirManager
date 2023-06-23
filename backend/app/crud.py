from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tasks).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Tasks).filter(models.Tasks.id == task_id).first()


def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Tasks(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



def update_task_is_done(db: Session, task_id: int):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    db_task.is_done = not db_task.is_done
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return db_task


# def update_task(db: Session, task: schemas.TaskUpdate, task_id: int):
#     db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
#     db_task.title = task.title
#     db_task.description = task.description
#     db_task.is_done = task.is_done
#     db_task.deadline = task.deadline
#     db.commit()
#     db.refresh(db_task)
#     return db_task


