from flask import Flask

from config import Config

from .db.connection import db_session


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if app.config.get("ADMIN_PASSWORD_HASH") is None:
        raise RuntimeError("ADMIN_PASSWORD_HASH is not configured.")
    if app.config.get("SECRET_KEY") is None:
        raise RuntimeError("SECRET_KEY is not configured.")

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # noqa: ARG001
        db_session.remove()

    from .categories.routes import categories_bp
    from .errors.handlers import errors
    from .main.routes import main_bp
    from .products.routes import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(errors)

    return app
