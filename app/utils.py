import secrets
from datetime import date, timedelta
from functools import wraps

from flask import g, redirect, session, url_for

from .db import get_db


MESI_IT = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]


def formatta_finestra_prevista(stima_da, stima_a):
    if not stima_da or not stima_a:
        return None
    da = date.fromisoformat(stima_da)
    a = date.fromisoformat(stima_a)
    mese_da = MESI_IT[da.month - 1]
    mese_a = MESI_IT[a.month - 1]
    if da.year == a.year:
        if mese_da == mese_a:
            return f"{mese_da} {da.year}"
        return f"{mese_da} e {mese_a} {da.year}"
    return f"{mese_da} {da.year} e {mese_a} {a.year}"


def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def get_current_user():
    if g.get("user") is None:
        user_id = session.get("user_id")
        if user_id is not None:
            db = get_db()
            g.user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        else:
            g.user = None
    return g.user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def onboarding_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return redirect(url_for("auth.login"))
        db = get_db()
        profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
        if profile is None or not profile["onboarding_completed"]:
            return redirect(url_for("onboarding.step1"))
        return view(*args, **kwargs)

    return wrapped


BADGE_LABELS = {
    "streak_10": "10 giorni di fila",
    "streak_30": "30 giorni di fila",
    "quiz_50": "50 risposte corrette",
    "quiz_200": "200 risposte corrette",
}


def touch_streak(db, user_id):
    """Aggiorna la streak giornaliera dell'utente e assegna eventuali badge."""
    today = date.today()
    row = db.execute("SELECT * FROM streaks WHERE user_id = ?", (user_id,)).fetchone()

    if row is None:
        db.execute(
            "INSERT INTO streaks (user_id, current_streak, longest_streak, last_activity_date) VALUES (?, 1, 1, ?)",
            (user_id, today.isoformat()),
        )
        db.commit()
        return

    last = date.fromisoformat(row["last_activity_date"]) if row["last_activity_date"] else None
    if last == today:
        return

    if last == today - timedelta(days=1):
        current = row["current_streak"] + 1
    else:
        current = 1

    longest = max(current, row["longest_streak"])
    db.execute(
        "UPDATE streaks SET current_streak = ?, longest_streak = ?, last_activity_date = ? WHERE user_id = ?",
        (current, longest, today.isoformat(), user_id),
    )

    if current == 10:
        award_badge(db, user_id, "streak_10")
    if current == 30:
        award_badge(db, user_id, "streak_30")

    db.commit()


def award_badge(db, user_id, codice):
    exists = db.execute(
        "SELECT 1 FROM badges WHERE user_id = ? AND codice = ?", (user_id, codice)
    ).fetchone()
    if not exists:
        db.execute(
            "INSERT INTO badges (user_id, codice, earned_at) VALUES (?, ?, ?)",
            (user_id, codice, date.today().isoformat()),
        )


def check_quiz_badges(db, user_id):
    total_correct = db.execute(
        "SELECT COALESCE(SUM(correct_count), 0) AS c FROM quiz_progress WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    if total_correct >= 50:
        award_badge(db, user_id, "quiz_50")
    if total_correct >= 200:
        award_badge(db, user_id, "quiz_200")
    db.commit()
