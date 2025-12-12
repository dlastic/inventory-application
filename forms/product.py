from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = DecimalField(
        "Price",
        validators=[InputRequired(), NumberRange(min=0)],
        render_kw={"step": "0.01"},
    )
    stock = IntegerField("Stock", validators=[InputRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", validators=[InputRequired()], coerce=int)
