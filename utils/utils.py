import os
import time
from functools import wraps
from typing import Callable

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

ADMIN_TTL_SECONDS = 10
try:
    ADMIN_PASSWORD_HASH: str = os.environ["ADMIN_PASSWORD_HASH"]
except KeyError:
    raise RuntimeError("ADMIN_PASSWORD_HASH environment variable not set.")


def _is_admin_valid() -> bool:
    if not session.get("is_admin"):
        return False
    if ADMIN_TTL_SECONDS is None:
        return True
    ts = session.get("is_admin_ts", 0)
    return (time.time() - ts) <= ADMIN_TTL_SECONDS


def _get_cancel_url(**kwargs) -> str:
    cancel_url = request.args.get("cancel")
    if cancel_url:
        return cancel_url

    if "category_id" in kwargs:
        return url_for("view_category", category_id=kwargs["category_id"])
    if "product_id" in kwargs:
        return url_for("view_product", product_id=kwargs["product_id"])

    return url_for("index")


def _verify_admin_password(entered_password: str) -> bool:
    return check_password_hash(ADMIN_PASSWORD_HASH, entered_password)


def require_admin_password(template: str = "admin_password_form.html") -> Callable:
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if _is_admin_valid():
                return f(*args, **kwargs)

            cancel_url = _get_cancel_url(**kwargs)

            if request.method == "GET":
                return render_template(template, cancel_url=cancel_url, **kwargs)

            if "admin_password" not in request.form:
                return render_template(template, cancel_url=cancel_url, **kwargs)

            entered_password = request.form.get("admin_password")
            if not entered_password or not _verify_admin_password(entered_password):
                flash("Invalid admin password.", "error")
                return render_template(template, cancel_url=cancel_url, **kwargs)

            session.clear()
            session["is_admin"] = True
            session["is_admin_ts"] = time.time()
            return redirect(request.path)

        return wrapped

    return decorator
