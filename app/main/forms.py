from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])


class DeleteForm(FlaskForm):
    pass
