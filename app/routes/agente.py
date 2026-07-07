from flask import Blueprint, render_template, request

from ..agente_engine import cerca
from ..db import get_db
from ..utils import login_required, onboarding_required

bp = Blueprint("agente", __name__, url_prefix="/agente")


@bp.route("/", methods=("GET", "POST"))
@login_required
@onboarding_required
def ask():
    risultati = []
    domanda = ""
    if request.method == "POST":
        domanda = request.form.get("domanda", "").strip()
        if domanda:
            db = get_db()
            bandi_rows = db.execute("SELECT * FROM bandi").fetchall()
            risultati = cerca(bandi_rows, domanda)

    return render_template("agente/ask.html", domanda=domanda, risultati=risultati)
