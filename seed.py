from app import app
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

u1 = User(
    username="awesome123",
    password=bcrypt.generate_password_hash("password"),
    email="user@email.com",
    first_name="Bob",
    last_name="Guy"
)

u2 = User(
    username="wow321",
    password=bcrypt.generate_password_hash("cool$tuff"),
    email="something@email.com",
    first_name="Joy",
    last_name="Totheworld"
)

db.session.add_all([u1, u2])
db.session.commit()
