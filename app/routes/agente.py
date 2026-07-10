from datetime import date, datetime

from flask import Blueprint, Response, current_app, redirect, render_template, request, stream_with_context, url_for

from ..ai_assistant import SYSTEM_PROMPT_BANDI_CHAT, stream_chat
from ..db import get_db, salva_messaggio_chat
from ..utils import get_current_user, login_required, onboarding_required

bp = Blueprint("agente", __name__, url_prefix="/agente")

CONTESTO = "bandi"


def _build_system_prompt(db):
    bandi_rows = db.execute("SELECT * FROM bandi").fetchall()
    blocchi = []
    for b in bandi_rows:
        blocchi.append(
            f"### {b['titolo']}\n"
            f"Corpo: {b['corpo']} | Categoria: {b['categoria']} | Posti: {b['posti']}\n"
            f"Pubblicato: {b['data_pubblicazione'] or 'n.d.'} | Apertura: {b['data_apertura'] or 'n.d.'} | "
            f"Scadenza: {b['data_scadenza'] or 'n.d.'}{' (STIMA, non ufficiale)' if b['stimato'] else ''}\n"
            f"Descrizione: {b['descrizione']}\n"
            f"Dettagli aggiuntivi: {b['testo_indicizzato']}\n"
            f"Fonte: {b['fonte_url']} ({b['fonte_tipo']})\n"
        )
    contesto = "\n".join(blocchi)
    oggi = f"Data di oggi: {date.today().isoformat()}. Usa questa data per stabilire se un bando è " \
        "attivo (scadenza futura), chiuso (scadenza passata) o previsto (nessuna data ancora nota)."
    return f"{SYSTEM_PROMPT_BANDI_CHAT}\n\n{oggi}\n\nCONTESTO (testi dei bandi indicizzati):\n{contesto}"


@bp.route("/")
@login_required
@onboarding_required
def ask():
    db = get_db()
    user = get_current_user()
    messaggi = db.execute(
        "SELECT * FROM chat_messages WHERE user_id = ? AND contesto = ? ORDER BY id ASC",
        (user["id"], CONTESTO),
    ).fetchall()
    return render_template(
        "agente/ask.html", messaggi=messaggi, ai_enabled=current_app.config["AI_ENABLED"]
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
    system_prompt = _build_system_prompt(db)
    api_key = current_app.config["ANTHROPIC_API_KEY"]
    db_path = current_app.config["DATABASE"]
    user_id = user["id"]

    def genera():
        pezzi = []
        for pezzo in stream_chat(api_key, system_prompt, messaggi_claude, abilita_ricerca_web=True):
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
    return redirect(url_for("agente.ask"))
