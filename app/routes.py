from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User, Post
import hashlib

main = Blueprint("main", __name__)


@main.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


@main.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@main.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    # Validation
    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user exists
    existing_user = User.query.filter(
        (User.username == data["username"]) | (User.email == data["email"])
    ).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Create user
    password_hash = hashlib.sha256(data.get("password", "").encode()).hexdigest()
    user = User(
        username=data["username"], email=data["email"], password_hash=password_hash
    )

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user"}), 500


@main.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@main.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "is_active" in data:
        user.is_active = data["is_active"]

    try:
        db.session.commit()
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update user"}), 500


@main.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete user"}), 500


@main.route("/api/users/<int:user_id>/posts", methods=["GET"])
def get_user_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return jsonify([post.to_dict() for post in posts])


@main.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    if (
        not data
        or "title" not in data
        or "content" not in data
        or "user_id" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    # Verify user exists
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    post = Post(title=data["title"], content=data["content"], user_id=data["user_id"])

    try:
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create post"}), 500
