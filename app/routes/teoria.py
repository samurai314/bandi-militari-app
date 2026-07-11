from flask import Blueprint, abort, render_template

from ..teoria_content import PILLOLE
from ..utils import login_required, onboarding_required

bp = Blueprint("teoria", __name__, url_prefix="/teoria")


@bp.route("/")
@login_required
@onboarding_required
def indice():
    materie = [(m, len(p)) for m, p in PILLOLE.items()]
    return render_template("teoria/indice.html", materie=materie)


@bp.route("/<materia>")
@login_required
@onboarding_required
def materia(materia):
    pillole = PILLOLE.get(materia)
    if not pillole:
        abort(404)
    return render_template("teoria/materia.html", materia=materia, pillole=pillole)
