from datetime import datetime

from flask import Blueprint, Response, current_app, redirect, render_template, request, stream_with_context, url_for

from ..ai_assistant import SYSTEM_PROMPT_COACH_FISICO, build_coach_context, stream_chat
from ..db import get_db, salva_messaggio_chat
from ..fisico_engine import genera_piano
from ..utils import get_current_user, login_required, onboarding_required

bp = Blueprint("coach", __name__, url_prefix="/fisico/coach")

CONTESTO = "coach_fisico"


def _build_system_prompt(db, user_id):
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    bando = None
    if profile["bando_id"]:
        bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()
    data_scadenza = bando["data_scadenza"] if bando else None
    piano = genera_piano(profile, data_scadenza)
    totale_sessioni = sum(len(w["giorni"]) for w in piano["settimane"])
    sessioni_fatte = db.execute(
        "SELECT COUNT(*) AS c FROM workout_log WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    streak = db.execute("SELECT * FROM streaks WHERE user_id = ?", (user_id,)).fetchone()

    contesto = build_coach_context(profile, piano, sessioni_fatte, totale_sessioni, streak)
    return f"{SYSTEM_PROMPT_COACH_FISICO}\n\nDATI UTENTE:\n{contesto}"


@bp.route("/")
@login_required
@onboarding_required
def home():
    db = get_db()
    user = get_current_user()
    messaggi = db.execute(
        "SELECT * FROM chat_messages WHERE user_id = ? AND contesto = ? ORDER BY id ASC",
        (user["id"], CONTESTO),
    ).fetchall()
    return render_template(
        "coach/chat.html", messaggi=messaggi, ai_enabled=current_app.config["AI_ENABLED"]
    )


@bp.route("/messaggio", methods=("POST",))
@login_required
@onboarding_required
def messaggio():
    db = get_db()
    user = get_current_user()
    testo_utente = request.form.get("messaggio", "").strip()

    if not testo_utente:
        return Response("", mimetype="text/plain")

    db.execute(
        "INSERT INTO chat_messages (user_id, contesto, ruolo, contenuto, timestamp) VALUES (?, ?, 'user', ?, ?)",
        (user["id"], CONTESTO, testo_utente, datetime.utcnow().isoformat()),
    )
    db.commit()

    storico_rows = db.execute(
        "SELECT ruolo, contenuto FROM chat_messages WHERE user_id = ? AND contesto = ? ORDER BY id ASC",
        (user["id"], CONTESTO),
    ).fetchall()
    messaggi_claude = [{"role": r["ruolo"], "content": r["contenuto"]} for r in storico_rows]
    system_prompt = _build_system_prompt(db, user["id"])
    api_key = current_app.config["ANTHROPIC_API_KEY"]
    db_path = current_app.config["DATABASE"]
    user_id = user["id"]

    def genera():
        pezzi = []
        for pezzo in stream_chat(api_key, system_prompt, messaggi_claude):
            pezzi.append(pezzo)
            yield pezzo
        risposta_completa = "".join(pezzi)
        salva_messaggio_chat(db_path, user_id, CONTESTO, "assistant", risposta_completa)

    return Response(stream_with_context(genera()), mimetype="text/plain")


@bp.route("/reset", methods=("POST",))
@login_required
@onboarding_required
def reset():
    db = get_db()
    user = get_current_user()
    db.execute("DELETE FROM chat_messages WHERE user_id = ? AND contesto = ?", (user["id"], CONTESTO))
    db.commit()
    return redirect(url_for("coach.home"))
