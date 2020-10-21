from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, NoteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

####################################################################
""" HOME ROUTES """


@app.route("/")
def redirect_to_register():
    """ redirects to register page """

    return render_template("home.html")


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


@app.route("/logout")
def logout():
    """ Logout User """

    session.pop("user_id")

    return redirect("/")

####################################################################
""" USER ROUTES """


@app.route("/users/<username>")
def show_user_details(username):
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


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete user"""

    user = User.query.get_or_404(username)

    # for note in user.notes:
    # db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")


####################################################################
""" NOTES ROUTES """


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_user_note(username):
    # user = User.query.filter_by(username=username).first()

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        note = Note(title=title, content=content, owner=username)

        db.session.add(note)
        db.session.commit()
        return redirect(f"/users/{username}")

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["user_id"] != username:
        flash("Not a valid user!")
        return redirect("/")
    else:
        return render_template("addnote.html", form=form, username=username)


@app.route("/notes/<note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    user = note.user
    form = NoteForm(title=note.title, content=note.content)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{user.username}")

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["user_id"] != user.username:
        flash("Not a valid user!")
        return redirect("/")
    else:
        return render_template("updatenote.html",
                               form=form,
                               note_id=note_id)


@app.route("/notes/<note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    user = note.user

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["user_id"] != user.username:
        flash("Not a valid user note!")
        return redirect("/")
    else:
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{user.username}")
