from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL, Email, Length
import email_validator


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=8, max=15, message="""Password must be between 8 and 15characters.""")])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in user"""

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class NoteForm(FlaskForm):
    """ Form for adding user notes"""

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])


