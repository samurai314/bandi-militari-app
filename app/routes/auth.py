from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db
from ..utils import get_current_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if get_current_user():
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        db = get_db()
        error = None

        if not email or not password:
            error = "Email e password sono obbligatorie."
        elif len(password) < 6:
            error = "La password deve avere almeno 6 caratteri."
        elif db.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
            error = "Esiste già un account con questa email."

        if error is None:
            cur = db.execute(
                "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                (email, generate_password_hash(password), datetime.utcnow().isoformat()),
            )
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            return redirect(url_for("onboarding.step1"))

        flash(error, "error")

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if get_current_user():
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        error = None

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Email o password non corretti."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("main.dashboard"))

        flash(error, "error")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
