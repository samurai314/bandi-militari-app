from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from ..db import get_db
from ..utils import get_current_user, login_required

bp = Blueprint("onboarding", __name__, url_prefix="/onboarding")


def _get_or_create_profile(db, user_id):
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    if profile is None:
        db.execute("INSERT INTO profiles (user_id) VALUES (?)", (user_id,))
        db.commit()
        profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    return profile


@bp.route("/step1", methods=("GET", "POST"))
@login_required
def step1():
    db = get_db()
    user = get_current_user()
    _get_or_create_profile(db, user["id"])

    q = request.args.get("q", "").strip()
    corpo_filtro = request.args.get("corpo", "")

    query = "SELECT * FROM bandi WHERE 1=1"
    params = []
    if q:
        query += " AND (titolo LIKE ? OR categoria LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if corpo_filtro:
        query += " AND corpo LIKE ?"
        params.append(f"%{corpo_filtro}%")
    query += " ORDER BY data_scadenza IS NULL, data_scadenza ASC"
    bandi = db.execute(query, params).fetchall()
    corpi = db.execute("SELECT DISTINCT corpo FROM bandi ORDER BY corpo").fetchall()

    if request.method == "POST":
        bando_id = request.form.get("bando_id")
        db.execute(
            "UPDATE profiles SET bando_id = ?, onboarding_step = 2 WHERE user_id = ?",
            (bando_id, user["id"]),
        )
        db.commit()
        return redirect(url_for("onboarding.step2"))

    return render_template("onboarding/step1.html", bandi=bandi, corpi=corpi, q=q, corpo_filtro=corpo_filtro)


@bp.route("/step2", methods=("GET", "POST"))
@login_required
def step2():
    db = get_db()
    user = get_current_user()
    profile = _get_or_create_profile(db, user["id"])
    if not profile["bando_id"]:
        return redirect(url_for("onboarding.step1"))

    if request.method == "POST":
        non_lo_so = 1 if request.form.get("non_lo_so") else 0
        db.execute(
            """UPDATE profiles SET
                sport = ?, sport_anni = ?, livello = ?,
                piegamenti = ?, trazioni = ?, corsa_distanza = ?, corsa_tempo_sec = ?,
                non_lo_so = ?, limitazioni = ?, onboarding_step = 3
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
        return redirect(url_for("onboarding.step3"))

    return render_template("onboarding/step2.html", profile=profile)


@bp.route("/step3", methods=("GET", "POST"))
@login_required
def step3():
    db = get_db()
    user = get_current_user()
    profile = _get_or_create_profile(db, user["id"])
    if not profile["bando_id"]:
        return redirect(url_for("onboarding.step1"))

    if request.method == "POST":
        db.execute(
            """UPDATE profiles SET
                contesto = ?, giorni_settimana = ?,
                onboarding_step = 4, onboarding_completed = 1, onboarding_completed_at = ?
               WHERE user_id = ?""",
            (
                request.form.get("contesto"),
                request.form.get("giorni_settimana"),
                datetime.utcnow().date().isoformat(),
                user["id"],
            ),
        )
        db.commit()
        return redirect(url_for("main.dashboard"))

    return render_template("onboarding/step3.html", profile=profile)
