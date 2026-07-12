from datetime import datetime

from flask import Blueprint, Response, current_app, redirect, render_template, request, stream_with_context, url_for

from ..ai_assistant import SYSTEM_PROMPT_COLLOQUIO_CHAT, TRIGGER_VALUTAZIONE_COLLOQUIO, stream_chat
from ..colloquio_engine import SEZIONI_ANSIA
from ..db import get_db, salva_messaggio_chat, salva_valutazione_colloquio
from ..utils import get_current_user, limite_ai_raggiunto, login_required, onboarding_required, touch_streak

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
    valutazioni = db.execute(
        """SELECT * FROM colloquio_log
           WHERE user_id = ? AND domanda = '__valutazione__'
           ORDER BY timestamp DESC LIMIT 5""",
        (user["id"],),
    ).fetchall()
    return render_template(
        "colloquio/intervista.html", messaggi=messaggi, valutazioni=valutazioni,
        ai_enabled=current_app.config["AI_ENABLED"],
        tts_enabled=current_app.config["TTS_ENABLED"],
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

    if limite_ai_raggiunto(db, user["id"]):
        return Response(
            "Hai raggiunto il limite giornaliero di messaggi per l'assistente AI. Riprova domani.",
            mimetype="text/plain",
        )

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

    e_valutazione = (testo_utente == TRIGGER_VALUTAZIONE_COLLOQUIO)

    def genera():
        pezzi = []
        for pezzo in stream_chat(api_key, SYSTEM_PROMPT_COLLOQUIO_CHAT, messaggi_claude):
            pezzi.append(pezzo)
            yield pezzo
        risposta_completa = "".join(pezzi)
        salva_messaggio_chat(db_path, user_id, CONTESTO, "assistant", risposta_completa)
        if e_valutazione and risposta_completa.strip():
            salva_valutazione_colloquio(db_path, user_id, risposta_completa)

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


@bp.route("/tts", methods=("POST",))
@login_required
@onboarding_required
def tts():
    """Sintesi vocale realistica via ElevenLabs (se configurata). Il testo è
    limitato per contenere i costi a crediti dell'account ElevenLabs."""
    if not current_app.config["TTS_ENABLED"]:
        return Response("TTS non configurato", status=503, mimetype="text/plain")

    testo = request.form.get("testo", "").strip()
    if not testo:
        return Response("", status=400, mimetype="text/plain")
    testo = testo[:900]

    import httpx

    voice_id = current_app.config["ELEVENLABS_VOICE_ID"]
    try:
        risposta = httpx.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": current_app.config["ELEVENLABS_API_KEY"],
                "Content-Type": "application/json",
            },
            json={
                "text": testo,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
            },
            timeout=30.0,
        )
        if risposta.status_code != 200:
            return Response("Errore dal servizio vocale", status=502, mimetype="text/plain")
        return Response(risposta.content, mimetype="audio/mpeg")
    except httpx.HTTPError:
        return Response("Servizio vocale non raggiungibile", status=502, mimetype="text/plain")


@bp.route("/ansia")
@login_required
@onboarding_required
def ansia():
    return render_template("colloquio/ansia.html", sezioni=SEZIONI_ANSIA)
