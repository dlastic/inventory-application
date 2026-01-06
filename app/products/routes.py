from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy.exc import IntegrityError

from ..db import queries
from ..main.utils import admin_required
from .forms import ProductForm
from .utils import handle_product_form

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/")
def list_products():
    products = queries.get_all_products()
    return render_template("products.html", products=products)


@products_bp.route("/<int:product_id>")
def view_product(product_id):
    product = queries.get_product_by_id(product_id)
    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("products.list_products"))

    return render_template("product.html", product=product)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    data, category_name = handle_product_form(form)

    if data:
        try:
            queries.add_product(**data)
            flash(
                f'Product "{data["name"]}" was successfully added to the "{category_name}" category.',
                "success",
            )
            return redirect(
                url_for("categories.view_category", category_id=data["category_id"])
            )
        except IntegrityError:
            flash(f'Product "{data["name"]}" already exists.', "error")

    selected_category_id = request.args.get("category_id", type=int)
    if request.method == "GET":
        form.category_id.data = (
            selected_category_id or current_app.config["DEFAULT_CATEGORY_ID"]
        )
    elif request.method == "POST":
        selected_category_id = form.category_id.data

    cancel_url = (
        url_for("categories.view_category", category_id=selected_category_id)
        if selected_category_id
        else url_for("products.list_products")
    )

    return render_template(
        "form.html",
        form=form,
        title="Add Product",
        button_text="Add Product",
        button_class="btn--add",
        cancel_url=cancel_url,
        action_url=url_for("products.add_product"),
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = queries.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products.list_products"))

    form = ProductForm()
    data, category_name = handle_product_form(form, product)

    if data:
        try:
            queries.update_product(product_id, **data)
            flash(
                f'Product "{data["name"]}" was successfully updated in the "{category_name}" category.',
                "success",
            )
            return redirect(url_for("products.view_product", product_id=product_id))
        except IntegrityError:
            flash(f'Product "{data["name"]}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title="Edit Product",
        button_text="Save Changes",
        button_class="btn--edit",
        cancel_url=url_for("products.view_product", product_id=product_id),
        action_url=url_for("products.edit_product", product_id=product_id),
    )


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = queries.get_product_by_id(product_id)
    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("products.list_products"))

    queries.delete_product(product_id)
    flash("Product deleted successfully.", "success")
    return redirect(
        url_for("categories.view_category", category_id=product.category_id)
    )
