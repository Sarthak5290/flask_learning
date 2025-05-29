from app import create_app, db
from app.models import User, Post
import os

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


if __name__ == "__main__":
    app.run(debug=True)
