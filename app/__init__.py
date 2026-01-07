from flask import Flask

from config import Config

from .db.connection import db_session


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
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
