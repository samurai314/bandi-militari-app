import json
from datetime import datetime

from flask import Blueprint, Response, flash, redirect, render_template, request, session, url_for

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
            sport = ?, sport_anni = ?, livello = ?, sesso = ?,
            piegamenti = ?, trazioni = ?, corsa_distanza = ?, corsa_tempo_sec = ?,
            non_lo_so = ?, limitazioni = ?
           WHERE user_id = ?""",
        (
            request.form.get("sport") or None,
            request.form.get("sport_anni") or None,
            request.form.get("livello") or None,
            request.form.get("sesso") or None,
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


@bp.route("/esporta")
@login_required
@onboarding_required
def esporta_dati():
    db = get_db()
    user = get_current_user()
    uid = user["id"]

    def righe(query, params=(uid,)):
        return [dict(r) for r in db.execute(query, params).fetchall()]

    dati = dict(
        esportato_il=datetime.utcnow().isoformat(),
        account=dict(email=user["email"], creato_il=user["created_at"]),
        profilo=righe("SELECT * FROM profiles WHERE user_id = ?"),
        progressi_quiz=righe("SELECT * FROM quiz_progress WHERE user_id = ?"),
        sessioni_quiz=righe("SELECT * FROM quiz_sessions_log WHERE user_id = ?"),
        checklist=righe("SELECT * FROM user_checklist WHERE user_id = ?"),
        streak=righe("SELECT * FROM streaks WHERE user_id = ?"),
        badge=righe("SELECT * FROM badges WHERE user_id = ?"),
        sessioni_allenamento=righe("SELECT * FROM workout_log WHERE user_id = ?"),
        colloqui=righe("SELECT * FROM colloquio_log WHERE user_id = ?"),
        conversazioni_ai=righe("SELECT * FROM chat_messages WHERE user_id = ?"),
    )
    corpo = json.dumps(dati, indent=2, ensure_ascii=False)
    return Response(
        corpo,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=i-miei-dati.json"},
    )


@bp.route("/elimina-account", methods=("POST",))
@login_required
@onboarding_required
def elimina_account():
    conferma = request.form.get("conferma", "").strip().lower()
    if conferma != "elimina":
        flash("Per confermare devi scrivere esattamente \"elimina\" nel campo richiesto.", "error")
        return redirect(url_for("impostazioni.index"))

    db = get_db()
    user = get_current_user()
    uid = user["id"]

    for tabella in (
        "quiz_progress", "quiz_sessions_log", "user_checklist", "streaks",
        "badges", "workout_log", "colloquio_log", "chat_messages", "profiles",
    ):
        db.execute(f"DELETE FROM {tabella} WHERE user_id = ?", (uid,))
    db.execute("DELETE FROM login_attempts WHERE email = ?", (user["email"],))
    db.execute("DELETE FROM users WHERE id = ?", (uid,))
    db.commit()

    session.clear()
    flash("Il tuo account e tutti i dati associati sono stati eliminati.", "success")
    return redirect(url_for("main.index"))
