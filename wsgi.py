from blog.app import create_app
from blog.models.database import db
from blog.models.users import User


app = create_app()


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    admin = User(user_name="admin", is_staff=True)
    james = User(user_name="james")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
