from datetime import date

from flask import Blueprint, abort, render_template, request

from ..db import get_db
from ..utils import login_required, onboarding_required

bp = Blueprint("bandi", __name__, url_prefix="/bandi")


def _stato(bando):
    if bando["stimato"]:
        return ("previsto", "Previsto / stima")
    if not bando["data_scadenza"]:
        return ("previsto", "Data da confermare")
    scadenza = date.fromisoformat(bando["data_scadenza"])
    if scadenza >= date.today():
        return ("attivo", "Attivo")
    return ("chiuso", "Chiuso")


@bp.route("/")
@login_required
@onboarding_required
def lista():
    db = get_db()
    filtro_stato = request.args.get("stato", "")
    rows = db.execute("SELECT * FROM bandi ORDER BY data_scadenza IS NULL, data_scadenza ASC").fetchall()

    bandi = []
    for b in rows:
        codice, label = _stato(b)
        if filtro_stato and filtro_stato != codice:
            continue
        giorni = None
        if b["data_scadenza"]:
            giorni = (date.fromisoformat(b["data_scadenza"]) - date.today()).days
        bandi.append(dict(row=b, stato_codice=codice, stato_label=label, giorni=giorni))

    return render_template("bandi/lista.html", bandi=bandi, filtro_stato=filtro_stato)


@bp.route("/<int:bando_id>")
@login_required
@onboarding_required
def dettaglio(bando_id):
    db = get_db()
    b = db.execute("SELECT * FROM bandi WHERE id = ?", (bando_id,)).fetchone()
    if b is None:
        abort(404)
    codice, label = _stato(b)
    giorni = None
    if b["data_scadenza"]:
        giorni = (date.fromisoformat(b["data_scadenza"]) - date.today()).days
    return render_template("bandi/dettaglio.html", b=b, stato_codice=codice, stato_label=label, giorni=giorni)
