from celery import Celery
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6373/0",
    backend="redis://localhost:6373/0"
)

@celery_app.task
def insert_user_task(name: str, surname: str):
    db = SessionLocal()
    try:
        new_user = models.User(name=name, surname=surname)
        db.add(new_user)
        db.commit()
        return f"User {name} {surname} saved successfully by Worker!"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        db.close()