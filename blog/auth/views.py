from blog.forms.user import RegistrationForm, LoginForm
from blog.models import User
from blog.models.database import db
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.exceptions import NotFound


auth = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@auth.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect("index")

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(user_name=form.user_name.data).count():
            form.user_name.errors.append("user_name already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            user_name=form.user_name.data,
            email=form.email.data,
            is_staff=False,
        )

        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("article.list"))

    return render_template("auth/register.html", form=form, error=error)


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
    if current_user.is_authenticated:
        return redirect("index")
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).one_or_none()
        if user is None:
            return render_template(
                "auth/login.html", form=form, error="user_name doesn't exist"
            )
        if not user.validate_password(form.password.data):
            return render_template(
                "auth/login.html", form=form, error="invalid user_name or password"
            )
        login_user(user)
        return redirect(url_for("article.list"))
    return render_template("auth/login.html", form=form)


@auth.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        # non-admin users should not know about this feature
        raise NotFound


@auth.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("article.list"))


@auth.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"
