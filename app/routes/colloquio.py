from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from ..colloquio_engine import DOMANDE, SEZIONI_ANSIA, analizza_risposta
from ..db import get_db
from ..utils import get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("colloquio", __name__, url_prefix="/colloquio")


@bp.route("/")
@login_required
@onboarding_required
def home():
    db = get_db()
    user = get_current_user()
    storico = db.execute(
        "SELECT * FROM colloquio_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5",
        (user["id"],),
    ).fetchall()
    return render_template("colloquio/home.html", domande=DOMANDE, storico=storico)


@bp.route("/simula", methods=("GET", "POST"))
@login_required
@onboarding_required
def simula():
    domanda = request.args.get("domanda") or (request.form.get("domanda") if request.method == "POST" else None)
    if not domanda:
        domanda = DOMANDE[0]

    feedback = None
    risposta = ""
    if request.method == "POST":
        risposta = request.form.get("risposta", "").strip()
        if risposta:
            feedback = analizza_risposta(risposta)
            db = get_db()
            user = get_current_user()
            db.execute(
                "INSERT INTO colloquio_log (user_id, domanda, risposta, timestamp) VALUES (?, ?, ?, ?)",
                (user["id"], domanda, risposta, datetime.utcnow().isoformat()),
            )
            db.commit()
            touch_streak(db, user["id"])

    return render_template(
        "colloquio/simula.html", domanda=domanda, domande=DOMANDE, feedback=feedback, risposta=risposta
    )


@bp.route("/ansia")
@login_required
@onboarding_required
def ansia():
    return render_template("colloquio/ansia.html", sezioni=SEZIONI_ANSIA)
