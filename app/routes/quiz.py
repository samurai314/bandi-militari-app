from datetime import date, datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

from ..db import get_db
from ..quiz_engine import materia_stats, pick_questions, review
from ..utils import check_quiz_badges, get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("quiz", __name__, url_prefix="/quiz")

MODE_LIMITS = {"practice": 10, "timed": 15, "simulation": 30}
MODE_SECONDS_PER_Q = {"practice": None, "timed": 45, "simulation": 60}


@bp.route("/")
@login_required
@onboarding_required
def home():
    db = get_db()
    user = get_current_user()
    stats = materia_stats(db, user["id"])
    materie = [s["materia"] for s in stats]
    return render_template("quiz/home.html", stats=stats, materie=materie)


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
        state["index"] += 1
        session["quiz_state"] = state

        if state["index"] >= len(state["question_ids"]):
            db.execute(
                "INSERT INTO quiz_sessions_log (user_id, mode, materia, total, correct, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (user["id"], state["mode"], state["materia"], len(state["question_ids"]), state["corrette"], datetime.utcnow().isoformat()),
            )
            db.commit()
            touch_streak(db, user["id"])
            check_quiz_badges(db, user["id"])
            return redirect(url_for("quiz.risultati"))

        return redirect(url_for("quiz.domanda"))

    question_id = state["question_ids"][state["index"]]
    q = db.execute("SELECT * FROM quiz_questions WHERE id = ?", (question_id,)).fetchone()
    return render_template(
        "quiz/domanda.html", q=q,
        numero=state["index"] + 1, totale=len(state["question_ids"]),
        secondi=state["secondi_per_domanda"], mode=state["mode"],
    )


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
    stats = materia_stats(db, user["id"])

    domande_deboli = db.execute(
        """SELECT q.domanda, q.materia, p.correct_count, p.attempts, p.next_review
           FROM quiz_progress p JOIN quiz_questions q ON q.id = p.question_id
           WHERE p.user_id = ? AND p.attempts > 0
           ORDER BY (CAST(p.correct_count AS FLOAT) / p.attempts) ASC, p.attempts DESC
           LIMIT 10""",
        (user["id"],),
    ).fetchall()

    return render_template("quiz/statistiche.html", stats=stats, domande_deboli=domande_deboli)
