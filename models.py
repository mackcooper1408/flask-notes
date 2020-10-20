from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    


def connect_db(app):
    db.app = app
    db.init_app(app)
