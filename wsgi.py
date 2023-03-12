from blog.app import create_app
from blog.models.database import db
from blog.models.users import User
import os


app = create_app()


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    flask create-admin
    > done! created users: <User #1 'admin'>
    """
    admin = User(user_name="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()

    print("created admin:", admin)


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag

    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
