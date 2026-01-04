from flask import request

from ..db import queries
from .forms import ProductForm


def handle_product_form(form: ProductForm, product=None, categories=None):
    if categories is None:
        categories = queries.get_all_categories()
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]

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
