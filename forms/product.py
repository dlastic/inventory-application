from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int)
