from datetime import datetime

from flask import Blueprint, Response, current_app, redirect, render_template, request, stream_with_context, url_for

from ..ai_assistant import SYSTEM_PROMPT_COLLOQUIO_CHAT, stream_chat
from ..colloquio_engine import SEZIONI_ANSIA
from ..db import get_db, salva_messaggio_chat
from ..utils import get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("colloquio", __name__, url_prefix="/colloquio")

CONTESTO = "colloquio"


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
        "colloquio/intervista.html", messaggi=messaggi, ai_enabled=current_app.config["AI_ENABLED"]
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
    touch_streak(db, user["id"])

    storico_rows = db.execute(
        "SELECT ruolo, contenuto FROM chat_messages WHERE user_id = ? AND contesto = ? ORDER BY id ASC",
        (user["id"], CONTESTO),
    ).fetchall()
    messaggi_claude = [{"role": r["ruolo"], "content": r["contenuto"]} for r in storico_rows]
    api_key = current_app.config["ANTHROPIC_API_KEY"]
    db_path = current_app.config["DATABASE"]
    user_id = user["id"]

    def genera():
        pezzi = []
        for pezzo in stream_chat(api_key, SYSTEM_PROMPT_COLLOQUIO_CHAT, messaggi_claude):
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
    return redirect(url_for("colloquio.home"))


@bp.route("/ansia")
@login_required
@onboarding_required
def ansia():
    return render_template("colloquio/ansia.html", sezioni=SEZIONI_ANSIA)
