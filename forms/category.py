from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()],)
