from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..db import get_db
from ..utils import get_current_user, login_required, onboarding_required

bp = Blueprint("impostazioni", __name__, url_prefix="/impostazioni")


@bp.route("/")
@login_required
@onboarding_required
def index():
    db = get_db()
    user = get_current_user()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()

    q = request.args.get("q", "").strip()
    query = "SELECT * FROM bandi WHERE 1=1"
    params = []
    if q:
        query += " AND (titolo LIKE ? OR categoria LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    query += " ORDER BY data_scadenza IS NULL, data_scadenza ASC"
    bandi = db.execute(query, params).fetchall()

    return render_template("impostazioni/index.html", profile=profile, bandi=bandi, q=q, user=user)


@bp.route("/bando", methods=("POST",))
@login_required
@onboarding_required
def cambia_bando():
    db = get_db()
    user = get_current_user()
    bando_id = request.form.get("bando_id")
    db.execute("UPDATE profiles SET bando_id = ? WHERE user_id = ?", (bando_id, user["id"]))
    db.commit()
    flash("Bando aggiornato.", "success")
    return redirect(url_for("impostazioni.index"))


@bp.route("/fisico", methods=("POST",))
@login_required
@onboarding_required
def aggiorna_fisico():
    db = get_db()
    user = get_current_user()
    non_lo_so = 1 if request.form.get("non_lo_so") else 0
    db.execute(
        """UPDATE profiles SET
            sport = ?, sport_anni = ?, livello = ?,
            piegamenti = ?, trazioni = ?, corsa_distanza = ?, corsa_tempo_sec = ?,
            non_lo_so = ?, limitazioni = ?
           WHERE user_id = ?""",
        (
            request.form.get("sport") or None,
            request.form.get("sport_anni") or None,
            request.form.get("livello") or None,
            request.form.get("piegamenti") or None,
            request.form.get("trazioni") or None,
            request.form.get("corsa_distanza") or None,
            request.form.get("corsa_tempo_sec") or None,
            non_lo_so,
            request.form.get("limitazioni") or None,
            user["id"],
        ),
    )
    db.commit()
    flash("Dati fisici aggiornati: il piano verrà ricalcolato.", "success")
    return redirect(url_for("impostazioni.index"))


@bp.route("/allenamento", methods=("POST",))
@login_required
@onboarding_required
def aggiorna_allenamento():
    db = get_db()
    user = get_current_user()
    db.execute(
        "UPDATE profiles SET contesto = ?, giorni_settimana = ?, settimane_preferite = ? WHERE user_id = ?",
        (
            request.form.get("contesto"),
            request.form.get("giorni_settimana"),
            request.form.get("settimane_preferite") or None,
            user["id"],
        ),
    )
    db.commit()
    flash("Preferenze di allenamento aggiornate.", "success")
    return redirect(url_for("impostazioni.index"))
