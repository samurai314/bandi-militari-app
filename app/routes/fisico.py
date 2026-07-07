from flask import Blueprint, render_template

from ..db import get_db
from ..fisico_engine import genera_piano
from ..utils import get_current_user, login_required, onboarding_required

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
    return render_template("fisico/piano.html", piano=piano, profile=profile, bando=bando)
