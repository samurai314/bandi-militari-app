from datetime import date

from flask import Blueprint, current_app, redirect, render_template, url_for

from ..db import get_db
from ..fisico_engine import classifica_livello, genera_piano
from ..quiz_engine import materia_stats
from ..readiness import calcola_prontezza, piano_di_oggi
from ..utils import BADGE_LABELS, get_current_user, login_required, onboarding_required

bp = Blueprint("main", __name__)


@bp.route("/sw.js")
def service_worker():
    return current_app.send_static_file("sw.js")


@bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@bp.route("/")
def index():
    user = get_current_user()
    if user is None:
        return render_template("index.html")

    db = get_db()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    if profile is None or not profile["onboarding_completed"]:
        return redirect(url_for("onboarding.step1"))
    return redirect(url_for("main.dashboard"))


@bp.route("/dashboard")
@login_required
@onboarding_required
def dashboard():
    user = get_current_user()
    db = get_db()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    bando = None
    giorni_countdown = None
    if profile["bando_id"]:
        bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()
        if bando and bando["data_scadenza"]:
            giorni_countdown = (date.fromisoformat(bando["data_scadenza"]) - date.today()).days

    settimana_fisico = 1
    if profile["onboarding_completed_at"]:
        giorni_passati = (date.today() - date.fromisoformat(profile["onboarding_completed_at"])).days
        settimana_fisico = max(1, giorni_passati // 7 + 1)

    livello = classifica_livello(profile) if profile["piegamenti"] is not None else "n.d."

    sessioni_fatte = db.execute(
        "SELECT COUNT(*) AS c FROM workout_log WHERE user_id = ?", (user["id"],)
    ).fetchone()["c"]

    totale_sessioni_fisico = 0
    piano_riepilogo = None
    if profile["piegamenti"] is not None:
        data_scadenza = bando["data_scadenza"] if bando else None
        piano_riepilogo = genera_piano(profile, data_scadenza)
        totale_sessioni_fisico = sum(len(w["giorni"]) for w in piano_riepilogo["settimane"])
    pct_fisico = round(100 * sessioni_fatte / totale_sessioni_fisico) if totale_sessioni_fisico else 0

    prontezza = calcola_prontezza(db, user["id"], totale_sessioni_fisico)
    azioni_oggi = piano_di_oggi(db, user["id"], settimana_fisico, piano_riepilogo)

    stats = materia_stats(db, user["id"], corpo_specifico=None)
    tentativi_totali = sum(s["tentativi"] for s in stats)
    corrette_totali = sum(s["corrette"] for s in stats)
    pct_quiz = round(100 * corrette_totali / tentativi_totali) if tentativi_totali else 0

    n_colloquio = db.execute(
        "SELECT COUNT(*) AS c FROM colloquio_log WHERE user_id = ?", (user["id"],)
    ).fetchone()["c"]

    streak = db.execute("SELECT * FROM streaks WHERE user_id = ?", (user["id"],)).fetchone()
    attivo_oggi = bool(streak and streak["last_activity_date"] == date.today().isoformat())
    badges = db.execute("SELECT * FROM badges WHERE user_id = ?", (user["id"],)).fetchall()
    badge_labels = [BADGE_LABELS.get(b["codice"], b["codice"]) for b in badges]

    checklist_totale = db.execute("SELECT COUNT(*) AS c FROM checklist_template").fetchone()["c"]
    checklist_fatti = db.execute(
        "SELECT COUNT(*) AS c FROM user_checklist WHERE user_id = ? AND checked = 1", (user["id"],)
    ).fetchone()["c"]
    pct_checklist = round(100 * checklist_fatti / checklist_totale) if checklist_totale else 0

    return render_template(
        "dashboard.html",
        bando=bando,
        giorni_countdown=giorni_countdown,
        settimana_fisico=settimana_fisico,
        livello=livello,
        sessioni_fatte=sessioni_fatte,
        totale_sessioni_fisico=totale_sessioni_fisico,
        pct_fisico=pct_fisico,
        pct_quiz=pct_quiz,
        pct_checklist=pct_checklist,
        tentativi_totali=tentativi_totali,
        n_colloquio=n_colloquio,
        streak=streak,
        attivo_oggi=attivo_oggi,
        badge_labels=badge_labels,
        checklist_totale=checklist_totale,
        checklist_fatti=checklist_fatti,
        prontezza=prontezza,
        azioni_oggi=azioni_oggi,
    )
