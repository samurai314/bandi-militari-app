from flask import Blueprint, current_app, render_template, request

from ..agente_engine import cerca
from ..ai_assistant import ask_bandi_assistant
from ..db import get_db
from ..utils import login_required, onboarding_required

bp = Blueprint("agente", __name__, url_prefix="/agente")


@bp.route("/", methods=("GET", "POST"))
@login_required
@onboarding_required
def ask():
    risultati = []
    risposta_ai = None
    errore_ai = None
    domanda = ""

    if request.method == "POST":
        domanda = request.form.get("domanda", "").strip()
        if domanda:
            db = get_db()
            bandi_rows = db.execute("SELECT * FROM bandi").fetchall()

            if current_app.config["AI_ENABLED"]:
                esito = ask_bandi_assistant(current_app.config["ANTHROPIC_API_KEY"], bandi_rows, domanda)
                if esito["ok"]:
                    risposta_ai = esito["testo"]
                else:
                    errore_ai = esito["error"]
                    risultati = cerca(bandi_rows, domanda)
            else:
                risultati = cerca(bandi_rows, domanda)

    return render_template(
        "agente/ask.html",
        domanda=domanda,
        risultati=risultati,
        risposta_ai=risposta_ai,
        errore_ai=errore_ai,
        ai_enabled=current_app.config["AI_ENABLED"],
    )
