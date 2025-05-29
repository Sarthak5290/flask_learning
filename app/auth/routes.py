from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.auth import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=request.form.get("remember_me"))
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.dashboard"))
            )

        flash("Invalid username or password")

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return render_template("auth/register.html")

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
