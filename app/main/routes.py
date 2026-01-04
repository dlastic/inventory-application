from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from .forms import LoginForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pwhash = current_app.config["ADMIN_PASSWORD_HASH"]
        password = form.password.data
        if check_password_hash(pwhash, password):
            session["is_admin"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))
        flash("Invalid password.", "error")
    return render_template(
        "form.html",
        form=form,
        title="Admin Login",
        button_text="Log In",
        button_class="btn--confirm",
        cancel_url=url_for("main.index"),
        action_url=url_for("main.login"),
    )


@main_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.index"))
