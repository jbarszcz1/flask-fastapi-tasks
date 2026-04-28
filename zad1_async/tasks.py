from celery import Celery
from models import db, User
from flask import Flask


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery


temp_app = Flask(__name__)
temp_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/users.db'
db.init_app(temp_app)
celery = make_celery(temp_app)


@celery.task
def insert_user_task(name, surname):
    with temp_app.app_context():
        try:
            new_user = User(name=name, surname=surname)
            db.session.add(new_user)
            db.session.commit()
            return f"User {name} {surname} saved successfully by Worker!"
        except Exception as e:
            db.session.rollback()
            return f"Error saving user: {str(e)}"
