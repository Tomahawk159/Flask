import os

from flask import Flask
from flask_migrate import Migrate

from blog.users.views import user
from blog.articles.views import article
from blog.models.database import db
from blog.auth.views import login_manager, auth
from blog.security import flask_bcrypt


basedir = os.path.abspath(os.path.dirname(__file__))


def create_app() -> Flask:
    app = Flask(__name__)

    cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
    cfg_name = 'BaseConfig'
    app.config.from_object(f"blog.configs.{cfg_name}")

    flask_bcrypt.init_app(app)
    db.init_app(app)

    migrate = Migrate(app, db)
    login_manager.init_app(app)
    register_blueprints(app)

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth)
