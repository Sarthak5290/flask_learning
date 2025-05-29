from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Todo
from app.main import bp


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    todos = (
        Todo.query.filter_by(user_id=current_user.id)
        .order_by(Todo.created_at.desc())
        .all()
    )

    # Statistics
    total_todos = len(todos)
    completed_todos = len([t for t in todos if t.completed])
    pending_todos = total_todos - completed_todos

    stats = {
        "total": total_todos,
        "completed": completed_todos,
        "pending": pending_todos,
    }

    return render_template("dashboard.html", todos=todos, stats=stats)


@bp.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    title = request.form["title"]
    description = request.form.get("description", "")
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date")

    todo = Todo(
        title=title,
        description=description,
        priority=priority,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None,
        user_id=current_user.id,
    )

    db.session.add(todo)
    db.session.commit()
    flash("Todo added successfully!")
    return redirect(url_for("main.dashboard"))


@bp.route("/edit_todo/<int:todo_id>", methods=["GET", "POST"])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        todo.title = request.form["title"]
        todo.description = request.form.get("description", "")
        todo.priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date")

        if due_date:
            todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        else:
            todo.due_date = None

        db.session.commit()
        flash("Todo updated successfully!")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_todo.html", todo=todo)


@bp.route("/toggle_todo/<int:todo_id>")
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("main.dashboard"))


@bp.route("/delete_todo/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully!")
    return redirect(url_for("main.dashboard"))
