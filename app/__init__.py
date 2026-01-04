from flask import Flask

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .categories.routes import categories_bp
    from .main.routes import main_bp
    from .products.routes import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)

    return app
