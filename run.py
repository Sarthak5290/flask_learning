from app import create_app, db
from app.models import User, Todo

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Todo": Todo}


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
