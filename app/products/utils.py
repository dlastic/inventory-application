from typing import Sequence

from flask import request

from ..db import queries
from ..db.models import Category, Product
from .forms import ProductForm


def handle_product_form(
    form: ProductForm,
    product: Product | None = None,
    categories: Sequence[Category] | None = None,
) -> tuple[dict, str | None] | tuple[None, None]:
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
        selected_category_name = next(
            (cat.name for cat in categories if cat.id == form.category_id.data), None
        )

        return data, selected_category_name
    return None, None
