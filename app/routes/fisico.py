from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from ..db import get_db
from ..fisico_engine import genera_piano
from ..utils import get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("fisico", __name__, url_prefix="/fisico")


@bp.route("/")
@login_required
@onboarding_required
def piano():
    db = get_db()
    user = get_current_user()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    bando = None
    if profile["bando_id"]:
        bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()

    data_scadenza = bando["data_scadenza"] if bando else None
    piano = genera_piano(profile, data_scadenza)

    completate_rows = db.execute(
        "SELECT settimana, giorno_indice FROM workout_log WHERE user_id = ?", (user["id"],)
    ).fetchall()
    completate = {(r["settimana"], r["giorno_indice"]) for r in completate_rows}

    totale_sessioni = sum(len(w["giorni"]) for w in piano["settimane"])

    return render_template(
        "fisico/piano.html", piano=piano, profile=profile, bando=bando,
        completate=completate, n_completate=len(completate), totale_sessioni=totale_sessioni,
    )


@bp.route("/completa", methods=("POST",))
@login_required
@onboarding_required
def completa():
    db = get_db()
    user = get_current_user()
    settimana = int(request.form["settimana"])
    giorno_indice = int(request.form["giorno_indice"])

    esiste = db.execute(
        "SELECT 1 FROM workout_log WHERE user_id = ? AND settimana = ? AND giorno_indice = ?",
        (user["id"], settimana, giorno_indice),
    ).fetchone()

    if esiste:
        db.execute(
            "DELETE FROM workout_log WHERE user_id = ? AND settimana = ? AND giorno_indice = ?",
            (user["id"], settimana, giorno_indice),
        )
    else:
        db.execute(
            "INSERT INTO workout_log (user_id, settimana, giorno_indice, completato_at) VALUES (?, ?, ?, ?)",
            (user["id"], settimana, giorno_indice, datetime.utcnow().isoformat()),
        )
        touch_streak(db, user["id"])

    db.commit()
    return redirect(url_for("fisico.piano") + f"#settimana-{settimana}")
