import os

from flask import Flask, flash, redirect, render_template, request, url_for

from db import queries
from utils.utils import require_admin_password

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/categories")
def list_categories():
    categories = queries.get_all_categories()
    return render_template("categories.html", categories=categories)


@app.route("/categories/<int:category_id>")
def view_category(category_id):
    category = queries.get_category_by_id(category_id)
    products = queries.get_products_by_category(category_id)
    return render_template("products.html", category=category, products=products)


@app.route("/categories/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        queries.add_category(name, description)
        flash(f'Category "{name}" was successfully created.', "success")
        return redirect(url_for("list_categories"))
    return render_template("add_category.html")


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@require_admin_password()
def edit_category(category_id):
    if category_id == 1:
        flash("The default category cannot be edited.", "error")
        return redirect(url_for("list_categories"))

    category = queries.get_category_by_id(category_id)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        queries.update_category(category_id, name, description)
        flash("Category updated successfully.", "success")

        return redirect(url_for("view_category", category_id=category_id))

    return render_template("edit_category.html", category=category)


@app.route("/categories/<int:category_id>/delete", methods=["POST"])
@require_admin_password(mode="delete")
def delete_category(category_id):
    if category_id == 1:
        flash("The default category cannot be deleted.", "error")
        return redirect(url_for("list_categories"))

    queries.delete_category(category_id)
    flash("Category deleted successfully.", "success")
    flash('Deleted products moved to default category ("Uncategorized")', "success")
    return redirect(url_for("list_categories"))


@app.route("/products")
def list_products():
    products = queries.get_all_products()
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>")
def view_product(product_id):
    product = queries.get_product_by_id(product_id)
    category = queries.get_category_by_id(product["category_id"])
    return render_template("product.html", product=product, category=category)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"] or None
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        category_id = (
            int(request.form["category_id"]) if request.form["category_id"] else None
        )
        category_name = queries.get_category_by_id(category_id)["name"]
        queries.add_product(name, description, price, stock, category_id)
        flash(
            f'Product "{name}" was successfully added to the "{category_name}" category.',
            "success",
        )
        return redirect(url_for("view_category", category_id=category_id))

    categories = queries.get_all_categories()
    selected_category_id = request.args.get("category_id", type=int)
    return render_template(
        "add_product.html",
        categories=categories,
        selected_category_id=selected_category_id,
    )


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@require_admin_password()
def edit_product(product_id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"] or None
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        category_id = (
            int(request.form["category_id"]) if request.form["category_id"] else None
        )
        queries.edit_product(product_id, name, description, price, stock, category_id)
        flash("Product updated successfully.", "success")
        return redirect(url_for("view_product", product_id=product_id))

    categories = queries.get_all_categories()
    product = queries.get_product_by_id(product_id)
    return render_template("edit_product.html", product=product, categories=categories)


@app.route("/products/<int:product_id>/delete", methods=["POST"])
@require_admin_password(mode="delete")
def delete_product(product_id):
    queries.delete_product(product_id)
    flash("Product deleted successfully.", "success")
    return redirect(url_for("list_products"))
