from datetime import date, datetime, timedelta

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

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


@bp.route("/chi-siamo")
def chi_siamo():
    return render_template("chi_siamo.html")


@bp.route("/feedback", methods=("GET", "POST"))
def feedback():
    if request.method == "POST":
        testo = request.form.get("testo", "").strip()
        if not testo:
            flash("Scrivi un messaggio prima di inviare.", "error")
            return redirect(url_for("main.feedback"))
        db = get_db()
        user = get_current_user()
        db.execute(
            "INSERT INTO feedback (user_id, email, testo, timestamp) VALUES (?, ?, ?, ?)",
            (
                user["id"] if user else None,
                (user["email"] if user else request.form.get("email", "").strip()) or None,
                testo[:2000],
                datetime.utcnow().isoformat(),
            ),
        )
        db.commit()
        flash("Grazie! Il tuo messaggio è stato ricevuto.", "success")
        return redirect(url_for("main.feedback"))
    return render_template("feedback.html")


@bp.route("/admin")
@login_required
def admin():
    """Pannello minimo per il gestore: visibile solo all'email indicata in ADMIN_EMAIL."""
    user = get_current_user()
    admin_email = current_app.config.get("ADMIN_EMAIL")
    if not admin_email or user["email"] != admin_email:
        abort(404)

    db = get_db()
    oggi = date.today().isoformat()
    stats = dict(
        utenti=db.execute("SELECT COUNT(*) c FROM users").fetchone()["c"],
        domande=db.execute("SELECT COUNT(*) c FROM quiz_questions").fetchone()["c"],
        risposte_totali=db.execute("SELECT COALESCE(SUM(attempts),0) c FROM quiz_progress").fetchone()["c"],
        sessioni_quiz_oggi=db.execute(
            "SELECT COUNT(*) c FROM quiz_sessions_log WHERE timestamp LIKE ?", (f"{oggi}%",)
        ).fetchone()["c"],
        messaggi_ai_oggi=db.execute(
            "SELECT COUNT(*) c FROM chat_messages WHERE ruolo='user' AND timestamp LIKE ?", (f"{oggi}%",)
        ).fetchone()["c"],
    )
    ultimi_feedback = db.execute(
        "SELECT * FROM feedback ORDER BY id DESC LIMIT 15"
    ).fetchall()
    return render_template("admin.html", stats=stats, ultimi_feedback=ultimi_feedback)


@bp.route("/demo")
def demo():
    """Quiz di prova accessibile senza registrazione: 5 domande con correzione
    lato client, per far provare l'app prima di creare un account."""
    db = get_db()
    domande = db.execute(
        "SELECT * FROM quiz_questions WHERE corpo_specifico IS NULL ORDER BY RANDOM() LIMIT 5"
    ).fetchall()
    return render_template("demo.html", domande=domande)


@bp.route("/scadenze")
def scadenze():
    """Bandi in scadenza nelle prossime settimane e aperture imminenti: pagina
    pubblica, è il tipo di informazione che serve anche prima di registrarsi."""
    db = get_db()
    oggi = date.today()
    rows = db.execute(
        "SELECT * FROM bandi WHERE data_scadenza IS NOT NULL ORDER BY data_scadenza ASC"
    ).fetchall()
    imminenti = []
    for b in rows:
        giorni = (date.fromisoformat(b["data_scadenza"]) - oggi).days
        if 0 <= giorni <= 30:
            imminenti.append(dict(row=b, giorni=giorni))
    previsti = db.execute(
        "SELECT * FROM bandi WHERE stimato = 1 ORDER BY stima_periodo_da ASC"
    ).fetchall()
    return render_template("scadenze.html", imminenti=imminenti, previsti=previsti)


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

    # Obiettivo giornaliero: domande risposte oggi rispetto al target scelto.
    obiettivo_giornaliero = profile["obiettivo_giornaliero"] or 20
    domande_oggi = db.execute(
        "SELECT COALESCE(SUM(total), 0) AS c FROM quiz_sessions_log WHERE user_id = ? AND timestamp >= ?",
        (user["id"], date.today().isoformat()),
    ).fetchone()["c"]

    # Calendario attività: quante attività (sessioni quiz, allenamenti,
    # scambi di colloquio) per ciascuno degli ultimi 84 giorni (12 settimane).
    inizio_calendario = (date.today() - timedelta(days=83)).isoformat()
    conteggi_giorno = {}
    for query in (
        "SELECT substr(timestamp, 1, 10) AS d, COUNT(*) AS n FROM quiz_sessions_log WHERE user_id = ? AND timestamp >= ? GROUP BY d",
        "SELECT substr(completato_at, 1, 10) AS d, COUNT(*) AS n FROM workout_log WHERE user_id = ? AND completato_at >= ? GROUP BY d",
        "SELECT substr(timestamp, 1, 10) AS d, COUNT(*) AS n FROM colloquio_log WHERE user_id = ? AND timestamp >= ? GROUP BY d",
    ):
        for r in db.execute(query, (user["id"], inizio_calendario)).fetchall():
            conteggi_giorno[r["d"]] = conteggi_giorno.get(r["d"], 0) + r["n"]

    calendario = []
    # Celle vuote iniziali per allineare il primo giorno al suo giorno della settimana.
    primo_giorno = date.today() - timedelta(days=83)
    calendario.extend([None] * primo_giorno.weekday())
    for i in range(83, -1, -1):
        g = date.today() - timedelta(days=i)
        n = conteggi_giorno.get(g.isoformat(), 0)
        intensita = 0 if n == 0 else (1 if n == 1 else (2 if n <= 3 else 3))
        calendario.append(dict(data=g.strftime("%d/%m"), n=n, intensita=intensita))

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
        obiettivo_giornaliero=obiettivo_giornaliero,
        domande_oggi=domande_oggi,
        calendario=calendario,
    )
