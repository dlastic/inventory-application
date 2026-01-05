from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from ..db import queries
from ..main.utils import admin_required
from .forms import CategoryForm

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
def list_categories():
    categories = queries.get_all_categories()
    return render_template("categories.html", categories=categories)


@categories_bp.route("/<int:category_id>")
def view_category(category_id):
    category = queries.get_category_by_id(category_id)
    return render_template(
        "products.html", category=category, products=category.products
    )


@categories_bp.route("/add", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            name, description = form.name.data, form.description.data
            queries.add_category(name, description)
            flash(f'Category "{name}" was successfully created.', "success")
            return redirect(url_for("categories.list_categories"))
        except IntegrityError:
            flash(f'Category "{name}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title="Add Category",
        button_text="Add Category",
        button_class="btn--add",
        cancel_url=url_for("categories.list_categories"),
        action_url=url_for("categories.add_category"),
    )


@categories_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_category(category_id):
    if category_id == current_app.config["DEFAULT_CATEGORY_ID"]:
        flash("The default category cannot be edited.", "error")
        return redirect(url_for("categories.list_categories"))

    category = queries.get_category_by_id(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        try:
            name, description = form.name.data, form.description.data
            queries.update_category(category_id, name, description)
            flash("Category updated successfully.", "success")
            return redirect(
                url_for("categories.view_category", category_id=category_id)
            )
        except IntegrityError:
            flash(f'Category "{name}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title=f"{category.name} – Edit Category",
        button_text="Edit Category",
        button_class="btn--edit",
        cancel_url=url_for("categories.view_category", category_id=category.id),
        action_url=url_for("categories.edit_category", category_id=category.id),
    )


@categories_bp.route("/<int:category_id>/delete", methods=["POST"])
@admin_required
def delete_category(category_id):
    if category_id == current_app.config["DEFAULT_CATEGORY_ID"]:
        flash("The default category cannot be deleted.", "error")
        return redirect(url_for("categories.list_categories"))

    count = queries.get_product_count_by_category(category_id)
    queries.delete_category(category_id)
    flash("Category deleted successfully.", "success")
    if count > 0:
        default_name = current_app.config["DEFAULT_CATEGORY_NAME"]
        flash(
            f'{count} deleted products moved to default category ("{default_name}")',
            "success",
        )
    return redirect(url_for("categories.list_categories"))
