import os
import time
from functools import wraps
from typing import Callable

from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash

ADMIN_TTL_SECONDS = 60
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")


def _is_admin_valid() -> bool:
    if not session.get("is_admin"):
        return False
    if ADMIN_TTL_SECONDS is None:
        return True
    ts = session.get("is_admin_ts", 0)
    return (time.time() - ts) <= ADMIN_TTL_SECONDS


def verify_admin_password(entered_password: str) -> bool:
    if not ADMIN_PASSWORD_HASH:
        return False
    return check_password_hash(ADMIN_PASSWORD_HASH, entered_password)


def require_admin_password(template: str = "admin_password_form.html") -> Callable:
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if _is_admin_valid():
                return f(*args, **kwargs)

            if request.method == "GET":
                return render_template(template, **kwargs)

            if "admin_password" not in request.form:
                return render_template(template, **kwargs)

            entered_password = request.form.get("admin_password")
            if not entered_password or not verify_admin_password(entered_password):
                flash("Invalid admin password.", "error")
                return render_template(template, **kwargs)

            session.clear()
            session["is_admin"] = True
            session["is_admin_ts"] = time.time()
            return redirect(request.path)

        return wrapped

    return decorator
