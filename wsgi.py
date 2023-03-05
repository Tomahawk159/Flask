from blog.app import create_app
from blog.models.database import db
from blog.models.users import User
import os


app = create_app()


# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()


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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
