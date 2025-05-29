from app import create_app, db
from app.models import User, Todo
from datetime import date


def init_database():
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Create a sample user for testing
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@example.com")
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()

            # Add sample todos
            sample_todos = [
                Todo(
                    title="Welcome to Todo App!",
                    description="This is your first todo item. You can edit or delete it.",
                    priority="high",
                    user_id=admin_user.id,
                ),
                Todo(
                    title="Buy groceries",
                    description="Milk, bread, eggs, and fruits",
                    priority="medium",
                    due_date=date.today(),
                    user_id=admin_user.id,
                ),
                Todo(
                    title="Finish project documentation",
                    description="Complete the API documentation for the new features",
                    priority="high",
                    user_id=admin_user.id,
                ),
                Todo(
                    title="Call dentist",
                    description="Schedule appointment for next month",
                    priority="low",
                    user_id=admin_user.id,
                ),
            ]

            for todo in sample_todos:
                db.session.add(todo)

            db.session.commit()
            print("Database initialized with sample data!")
            print("Login credentials:")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Database already initialized!")


if __name__ == "__main__":
    init_database()
