from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model):
    """ User SQLA Class """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ has password and register new user """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")

        return cls(username=username,
                   password=hashed_pwd,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)


def connect_db(app):
    db.app = app
    db.init_app(app)
