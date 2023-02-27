from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from blog.models import User

auth = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


__all__ = [
    "login_manager",
    "auth",
]


@auth.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    user_name = request.form.get("user_name")

    if not user_name:
        return render_template("auth/login.html", error="user_name not passed")
    user = User.query.filter_by(user_name=user_name).one_or_none()

    if user is None:
        return render_template("auth/login.html", error=f"no user {user_name!r} found")
    login_user(user)
    return redirect(url_for("index"))


@auth.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"
