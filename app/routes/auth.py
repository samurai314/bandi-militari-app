import secrets
from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db
from ..utils import get_current_user

bp = Blueprint("auth", __name__, url_prefix="/auth")

MAX_TENTATIVI_LOGIN = 5
BLOCCO_MINUTI = 15


def genera_codice_recupero():
    """Codice leggibile tipo A3F9-K2M7 (senza caratteri ambigui)."""
    alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    blocco = lambda: "".join(secrets.choice(alfabeto) for _ in range(4))
    return f"{blocco()}-{blocco()}"


def _stato_blocco(db, email):
    """Ritorna il numero di minuti residui di blocco per questa email, o None se non bloccata."""
    row = db.execute("SELECT * FROM login_attempts WHERE email = ?", (email,)).fetchone()
    if row is None or not row["bloccato_fino"]:
        return None
    bloccato_fino = datetime.fromisoformat(row["bloccato_fino"])
    if datetime.utcnow() >= bloccato_fino:
        return None
    minuti_residui = int((bloccato_fino - datetime.utcnow()).total_seconds() // 60) + 1
    return minuti_residui


def _registra_tentativo_fallito(db, email):
    row = db.execute("SELECT * FROM login_attempts WHERE email = ?", (email,)).fetchone()
    tentativi = (row["tentativi"] if row else 0) + 1
    bloccato_fino = None
    if tentativi >= MAX_TENTATIVI_LOGIN:
        bloccato_fino = (datetime.utcnow() + timedelta(minutes=BLOCCO_MINUTI)).isoformat()
        tentativi = 0
    if row:
        db.execute(
            "UPDATE login_attempts SET tentativi = ?, ultimo_tentativo = ?, bloccato_fino = ? WHERE email = ?",
            (tentativi, datetime.utcnow().isoformat(), bloccato_fino, email),
        )
    else:
        db.execute(
            "INSERT INTO login_attempts (email, tentativi, ultimo_tentativo, bloccato_fino) VALUES (?, ?, ?, ?)",
            (email, tentativi, datetime.utcnow().isoformat(), bloccato_fino),
        )
    db.commit()


def _azzera_tentativi(db, email):
    db.execute("DELETE FROM login_attempts WHERE email = ?", (email,))
    db.commit()


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
            codice = genera_codice_recupero()
            cur = db.execute(
                "INSERT INTO users (email, password_hash, created_at, recovery_code_hash) VALUES (?, ?, ?, ?)",
                (email, generate_password_hash(password), datetime.utcnow().isoformat(),
                 generate_password_hash(codice)),
            )
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            # Mostrato una sola volta: senza email di conferma è l'unico modo
            # per recuperare l'account se dimentichi la password.
            return render_template("auth/codice_recupero.html", codice=codice, nuovo_account=True)

        flash(error, "error")

    return render_template("auth/register.html")


@bp.route("/recupero", methods=("GET", "POST"))
def recupero():
    if get_current_user():
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        codice = request.form.get("codice", "").strip().upper()
        nuova_password = request.form.get("nuova_password", "")
        db = get_db()
        error = None

        minuti_residui = _stato_blocco(db, email)
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if minuti_residui is not None:
            error = f"Troppi tentativi falliti. Riprova tra circa {minuti_residui} minuti."
        elif len(nuova_password) < 6:
            error = "La nuova password deve avere almeno 6 caratteri."
        elif (
            user is None
            or not user["recovery_code_hash"]
            or not check_password_hash(user["recovery_code_hash"], codice)
        ):
            error = "Email o codice di recupero non corretti."
            _registra_tentativo_fallito(db, email)

        if error is None:
            nuovo_codice = genera_codice_recupero()
            db.execute(
                "UPDATE users SET password_hash = ?, recovery_code_hash = ? WHERE id = ?",
                (generate_password_hash(nuova_password), generate_password_hash(nuovo_codice), user["id"]),
            )
            db.commit()
            _azzera_tentativi(db, email)
            session.clear()
            session["user_id"] = user["id"]
            flash("Password reimpostata. Il vecchio codice non è più valido: salva quello nuovo.", "success")
            return render_template("auth/codice_recupero.html", codice=nuovo_codice, nuovo_account=False)

        flash(error, "error")

    return render_template("auth/recupero.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if get_current_user():
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        db = get_db()
        error = None

        minuti_residui = _stato_blocco(db, email)
        if minuti_residui is not None:
            error = (
                f"Troppi tentativi falliti. Riprova tra circa {minuti_residui} minuti "
                "per motivi di sicurezza."
            )
        else:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if user is None or not check_password_hash(user["password_hash"], password):
                error = "Email o password non corretti."
                _registra_tentativo_fallito(db, email)

        if error is None:
            _azzera_tentativi(db, email)
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("main.dashboard"))

        flash(error, "error")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
