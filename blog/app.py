from flask import Flask, render_template
from blog.users.views import user
from blog.articles.views import article
from blog.models.database import db
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
        os.path.join(basedir, 'blog.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(article)
