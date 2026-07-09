from datetime import datetime

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from ..ai_assistant import ai_feedback_colloquio
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
    feedback_ai = None
    risposta = ""
    if request.method == "POST":
        risposta = request.form.get("risposta", "").strip()
        if risposta:
            feedback = analizza_risposta(risposta)

            if current_app.config["AI_ENABLED"]:
                esito = ai_feedback_colloquio(current_app.config["ANTHROPIC_API_KEY"], domanda, risposta)
                if esito["ok"]:
                    feedback_ai = esito["testo"]

            db = get_db()
            user = get_current_user()
            db.execute(
                "INSERT INTO colloquio_log (user_id, domanda, risposta, timestamp) VALUES (?, ?, ?, ?)",
                (user["id"], domanda, risposta, datetime.utcnow().isoformat()),
            )
            db.commit()
            touch_streak(db, user["id"])

    return render_template(
        "colloquio/simula.html", domanda=domanda, domande=DOMANDE, feedback=feedback,
        feedback_ai=feedback_ai, risposta=risposta, ai_enabled=current_app.config["AI_ENABLED"],
    )


@bp.route("/ansia")
@login_required
@onboarding_required
def ansia():
    return render_template("colloquio/ansia.html", sezioni=SEZIONI_ANSIA)
