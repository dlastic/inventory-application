from flask import Flask, redirect, render_template, request, url_for

from db.queries import (
    add_category,
    get_all_categories,
    get_all_products,
    get_category_by_id,
    get_product_by_id,
    get_products_by_category,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/categories")
def list_categories():
    categories = get_all_categories()
    return render_template("categories.html", categories=categories)


@app.route("/categories/<int:category_id>")
def view_category(category_id):
    category = get_category_by_id(category_id)
    products = get_products_by_category(category_id)
    return render_template("products.html", category=category, products=products)


@app.route("/categories/add", methods=["GET", "POST"])
def new_category():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        add_category(name, description)
        return redirect(url_for("list_categories"))
    return render_template("add_category.html")


@app.route("/products")
def list_products():
    products = get_all_products()
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>")
def view_product(product_id):
    product = get_product_by_id(product_id)
    return render_template("product.html", product=product)
