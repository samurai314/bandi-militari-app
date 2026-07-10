from datetime import date, datetime, timedelta

from flask import Blueprint, redirect, render_template, request, session, url_for

from ..db import get_db
from ..quiz_engine import conta_errori, corpo_specifico_per_bando, materia_stats, pick_questions, review
from ..utils import check_quiz_badges, get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("quiz", __name__, url_prefix="/quiz")

MODE_LIMITS = {"practice": 10, "prova": 10, "timed": 15, "simulation": 30, "errori": 20}
MODE_SECONDS_PER_Q = {"practice": None, "prova": None, "timed": 45, "simulation": 60, "errori": None}


def _corpo_tag_utente(db, user_id):
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not profile or not profile["bando_id"]:
        return None
    bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()
    return corpo_specifico_per_bando(bando["corpo"]) if bando else None


def _termina_sessione(db, user, state):
    db.execute(
        "INSERT INTO quiz_sessions_log (user_id, mode, materia, total, correct, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (user["id"], state["mode"], state["materia"], len(state["question_ids"]), state["corrette"], datetime.utcnow().isoformat()),
    )
    db.commit()
    touch_streak(db, user["id"])
    check_quiz_badges(db, user["id"])


@bp.route("/")
@login_required
@onboarding_required
def home():
    db = get_db()
    user = get_current_user()
    corpo_tag = _corpo_tag_utente(db, user["id"])
    stats_generiche = materia_stats(db, user["id"])
    stats_specifiche = materia_stats(db, user["id"], corpo_specifico=corpo_tag) if corpo_tag else []
    n_errori = conta_errori(db, user["id"])
    return render_template(
        "quiz/home.html", stats_generiche=stats_generiche, stats_specifiche=stats_specifiche,
        corpo_tag=corpo_tag, n_errori=n_errori,
    )


@bp.route("/avvia")
@login_required
@onboarding_required
def avvia():
    db = get_db()
    user = get_current_user()
    mode = request.args.get("mode", "practice")
    materia = request.args.get("materia") or None
    limit = MODE_LIMITS.get(mode, 10)

    domande = pick_questions(db, user["id"], materia=materia, limit=limit, mode=mode)
    if not domande:
        return redirect(url_for("quiz.home"))

    session["quiz_state"] = dict(
        mode=mode,
        materia=materia,
        question_ids=[d["id"] for d in domande],
        index=0,
        corrette=0,
        risposte=[],
        secondi_per_domanda=MODE_SECONDS_PER_Q.get(mode),
        in_attesa_conferma=False,
        ultimo_feedback=None,
    )
    return redirect(url_for("quiz.domanda"))


@bp.route("/domanda", methods=("GET", "POST"))
@login_required
@onboarding_required
def domanda():
    state = session.get("quiz_state")
    if not state:
        return redirect(url_for("quiz.home"))

    db = get_db()
    user = get_current_user()

    if request.method == "POST":
        question_id = state["question_ids"][state["index"]]
        risposta_data = request.form.get("risposta")
        q = db.execute("SELECT * FROM quiz_questions WHERE id = ?", (question_id,)).fetchone()
        corretto = (risposta_data == q["risposta"])

        progress = db.execute(
            "SELECT * FROM quiz_progress WHERE user_id = ? AND question_id = ?",
            (user["id"], question_id),
        ).fetchone()
        rep = progress["repetitions"] if progress else 0
        interval = progress["interval_days"] if progress else 0
        ease = progress["ease_factor"] if progress else 2.5

        rep, interval, ease, next_review = review(rep, interval, ease, corretto)

        if progress:
            db.execute(
                """UPDATE quiz_progress SET repetitions=?, interval_days=?, ease_factor=?, next_review=?,
                   last_result=?, attempts=attempts+1, correct_count=correct_count+?
                   WHERE user_id=? AND question_id=?""",
                (rep, interval, ease, next_review, int(corretto), int(corretto), user["id"], question_id),
            )
        else:
            db.execute(
                """INSERT INTO quiz_progress
                   (user_id, question_id, repetitions, interval_days, ease_factor, next_review,
                    last_result, attempts, correct_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)""",
                (user["id"], question_id, rep, interval, ease, next_review, int(corretto), int(corretto)),
            )
        db.commit()

        state["corrette"] += int(corretto)
        state["risposte"].append(dict(
            question_id=question_id, corretto=corretto, risposta_data=risposta_data,
            risposta_giusta=q["risposta"], spiegazione=q["spiegazione"], domanda=q["domanda"],
        ))

        if state["mode"] == "prova":
            state["in_attesa_conferma"] = True
            state["ultimo_feedback"] = dict(
                corretto=corretto, risposta_data=risposta_data,
                risposta_giusta=q["risposta"], spiegazione=q["spiegazione"],
            )
            session["quiz_state"] = state
            return redirect(url_for("quiz.domanda"))

        state["index"] += 1
        session["quiz_state"] = state

        if state["index"] >= len(state["question_ids"]):
            _termina_sessione(db, user, state)
            return redirect(url_for("quiz.risultati"))

        return redirect(url_for("quiz.domanda"))

    question_id = state["question_ids"][state["index"]]
    q = db.execute("SELECT * FROM quiz_questions WHERE id = ?", (question_id,)).fetchone()
    return render_template(
        "quiz/domanda.html", q=q,
        numero=state["index"] + 1, totale=len(state["question_ids"]),
        secondi=state["secondi_per_domanda"], mode=state["mode"],
        in_attesa_conferma=state.get("in_attesa_conferma", False),
        ultimo_feedback=state.get("ultimo_feedback"),
    )


@bp.route("/avanti", methods=("POST",))
@login_required
@onboarding_required
def avanti():
    state = session.get("quiz_state")
    if not state:
        return redirect(url_for("quiz.home"))

    db = get_db()
    user = get_current_user()

    state["in_attesa_conferma"] = False
    state["ultimo_feedback"] = None
    state["index"] += 1
    session["quiz_state"] = state

    if state["index"] >= len(state["question_ids"]):
        _termina_sessione(db, user, state)
        return redirect(url_for("quiz.risultati"))

    return redirect(url_for("quiz.domanda"))


@bp.route("/risultati")
@login_required
@onboarding_required
def risultati():
    state = session.get("quiz_state")
    if not state:
        return redirect(url_for("quiz.home"))
    return render_template("quiz/risultati.html", state=state)


@bp.route("/statistiche")
@login_required
@onboarding_required
def statistiche():
    db = get_db()
    user = get_current_user()
    corpo_tag = _corpo_tag_utente(db, user["id"])
    stats_generiche = materia_stats(db, user["id"])
    stats_specifiche = materia_stats(db, user["id"], corpo_specifico=corpo_tag) if corpo_tag else []

    domande_deboli = db.execute(
        """SELECT q.domanda, q.materia, p.correct_count, p.attempts, p.next_review
           FROM quiz_progress p JOIN quiz_questions q ON q.id = p.question_id
           WHERE p.user_id = ? AND p.attempts > 0
           ORDER BY (CAST(p.correct_count AS FLOAT) / p.attempts) ASC, p.attempts DESC
           LIMIT 10""",
        (user["id"],),
    ).fetchall()

    n_errori = conta_errori(db, user["id"])

    classifica = []
    profile = db.execute("SELECT bando_id FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    if profile and profile["bando_id"]:
        una_settimana_fa = (datetime.utcnow() - timedelta(days=7)).isoformat()
        righe = db.execute(
            """SELECT qsl.user_id, SUM(qsl.correct) AS punteggio
               FROM quiz_sessions_log qsl
               JOIN profiles pr ON pr.user_id = qsl.user_id
               WHERE pr.bando_id = ? AND qsl.timestamp >= ?
               GROUP BY qsl.user_id
               ORDER BY punteggio DESC
               LIMIT 10""",
            (profile["bando_id"], una_settimana_fa),
        ).fetchall()
        for i, r in enumerate(righe, start=1):
            sei_tu = (r["user_id"] == user["id"])
            classifica.append(dict(
                posizione=i, punteggio=r["punteggio"],
                etichetta="Tu" if sei_tu else f"Candidato #{i}", sei_tu=sei_tu,
            ))

    return render_template(
        "quiz/statistiche.html", stats_generiche=stats_generiche, stats_specifiche=stats_specifiche,
        domande_deboli=domande_deboli, n_errori=n_errori, classifica=classifica,
    )
