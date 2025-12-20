from flask import request
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

from db import queries


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


def handle_product_form(form: ProductForm, product=None, categories=None):
    if categories is None:
        categories = queries.get_all_categories()
    form.category_id.choices = [(cat["id"], cat["name"]) for cat in categories]

    if product and request.method == "GET":
        form.process(obj=product)

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data,
            "price": form.price.data,
            "stock": form.stock.data,
            "category_id": form.category_id.data,
        }
        category_name = next(
            (
                choice[1]
                for choice in form.category_id.choices
                if choice[0] == form.category_id.data
            ),
            None,
        )

        return data, category_name
    return None, None
