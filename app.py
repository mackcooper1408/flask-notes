from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def redirect_to_register():
    """ redirects to register page """

    return redirect("/register")


@app.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register_user():
    """ Show and process registration form """
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username,
                             password=password,
                             email=email,
                             first_name=first_name,
                             last_name=last_name)

        if user:
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["invalid username or password"]
    return render_template("register.html", form=form)


@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """ Show and login user"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["invalid username or password"]
    return render_template("login.html", form=form)


@app.route("/users/<username>")
def secret(username):
    """ Show user page """
    user = User.query.filter_by(username=username).first()

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["user_id"] != username:
        flash("Not a valid user!")
        return redirect("/")
    else:
        return render_template("user.html", user=user)


@app.route("/logout")
def logout():
    """ Logout User """

    session.pop("user_id")

    return redirect("/")
