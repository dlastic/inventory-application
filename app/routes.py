from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from app import app

from .db import queries
from .forms import CategoryForm, LoginForm, ProductForm, handle_product_form
from .utils.utils import admin_required


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pwhash = app.config["ADMIN_PASSWORD_HASH"]
        password = form.password.data
        if check_password_hash(pwhash, password):
            session["is_admin"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("index"))
        flash("Invalid password.", "error")
    return render_template(
        "form.html",
        form=form,
        title="Admin Login",
        button_text="Log In",
        button_class="btn--confirm",
        cancel_url=url_for("index"),
        action_url=url_for("login"),
    )


@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


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
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            name, description = form.name.data, form.description.data
            queries.add_category(name, description)
            flash(f'Category "{name}" was successfully created.', "success")
            return redirect(url_for("list_categories"))
        except IntegrityError:
            flash(f'Category "{name}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title="Add Category",
        button_text="Add Category",
        button_class="btn--add",
        cancel_url=url_for("list_categories"),
        action_url=url_for("add_category"),
    )


@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_category(category_id):
    if category_id == 1:
        flash("The default category cannot be edited.", "error")
        return redirect(url_for("list_categories"))

    category = queries.get_category_by_id(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        try:
            name, description = form.name.data, form.description.data
            queries.update_category(category_id, name, description)
            flash("Category updated successfully.", "success")
            return redirect(url_for("view_category", category_id=category_id))
        except IntegrityError:
            flash(f'Category "{name}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title=f"{category.name} – Edit Category",
        button_text="Edit Category",
        button_class="btn--edit",
        cancel_url=url_for("view_category", category_id=category.id),
        action_url=url_for("edit_category", category_id=category.id),
    )


@app.route("/categories/<int:category_id>/delete", methods=["POST"])
@admin_required
def delete_category(category_id):
    if category_id == 1:
        flash("The default category cannot be deleted.", "error")
        return redirect(url_for("list_categories"))

    count = queries.get_product_count_by_category(category_id)
    queries.delete_category(category_id)
    flash("Category deleted successfully.", "success")
    if count > 0:
        flash(
            f'{count} deleted products moved to default category ("Uncategorized")',
            "success",
        )
    return redirect(url_for("list_categories"))


@app.route("/products")
def list_products():
    products = queries.get_all_products()
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>")
def view_product(product_id):
    product = queries.get_product_by_id(product_id)
    category = queries.get_category_by_id(product.category_id)
    return render_template("product.html", product=product, category=category)


@app.route("/products/add", methods=["GET", "POST"])
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
            return redirect(url_for("view_category", category_id=data["category_id"]))
        except IntegrityError:
            flash(f'Product "{data["name"]}" already exists.', "error")

    selected_category_id = request.args.get("category_id", type=int)
    if request.method == "GET":
        form.category_id.data = selected_category_id or 1
    elif request.method == "POST":
        selected_category_id = form.category_id.data

    cancel_url = (
        url_for("view_category", category_id=selected_category_id)
        if selected_category_id
        else url_for("list_products")
    )

    return render_template(
        "form.html",
        form=form,
        title="Add Product",
        button_text="Add Product",
        button_class="btn--add",
        cancel_url=cancel_url,
        action_url=url_for("add_product"),
    )


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = queries.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("list_products"))

    form = ProductForm()
    data, category_name = handle_product_form(form, product)

    if data:
        try:
            queries.update_product(product_id, **data)
            flash(
                f'Product "{data["name"]}" was successfully updated in the "{category_name}" category.',
                "success",
            )
            return redirect(url_for("view_product", product_id=product_id))
        except IntegrityError:
            flash(f'Product "{data["name"]}" already exists.', "error")

    return render_template(
        "form.html",
        form=form,
        title="Edit Product",
        button_text="Save Changes",
        button_class="btn--edit",
        cancel_url=url_for("view_product", product_id=product_id),
        action_url=url_for("edit_product", product_id=product_id),
    )


@app.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = queries.get_product_by_id(product_id)
    queries.delete_product(product_id)
    flash("Product deleted successfully.", "success")
    return redirect(url_for("view_category", category_id=product.category_id))
