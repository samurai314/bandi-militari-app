import time
from datetime import datetime, timedelta

from flask import Blueprint, Response, current_app, redirect, render_template, request, session, stream_with_context, url_for

from ..ai_assistant import SYSTEM_PROMPT_RIPASSO, stream_chat
from ..db import get_db
from ..quiz_engine import (
    FORMATI_ESAME,
    conta_errori,
    corpo_specifico_per_bando,
    materia_stats,
    pick_questions,
    pick_questions_esame,
    review,
)
from ..utils import (
    check_quiz_badges,
    get_current_user,
    limite_ai_raggiunto,
    login_required,
    onboarding_required,
    touch_streak,
)

bp = Blueprint("quiz", __name__, url_prefix="/quiz")

MODE_LIMITS = {"practice": 10, "prova": 10, "timed": 15, "simulation": 30, "errori": 20}
MODE_SECONDS_PER_Q = {"practice": None, "prova": None, "timed": 45, "simulation": 60, "errori": None}


def _corpo_tag_utente(db, user_id):
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not profile or not profile["bando_id"]:
        return None
    bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()
    return corpo_specifico_per_bando(bando["corpo"]) if bando else None


def _aggiorna_progresso(db, user_id, question_id, corretto):
    progress = db.execute(
        "SELECT * FROM quiz_progress WHERE user_id = ? AND question_id = ?",
        (user_id, question_id),
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
            (rep, interval, ease, next_review, int(corretto), int(corretto), user_id, question_id),
        )
    else:
        db.execute(
            """INSERT INTO quiz_progress
               (user_id, question_id, repetitions, interval_days, ease_factor, next_review,
                last_result, attempts, correct_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)""",
            (user_id, question_id, rep, interval, ease, next_review, int(corretto), int(corretto)),
        )
    db.commit()


def _termina_sessione(db, user, state):
    db.execute(
        "INSERT INTO quiz_sessions_log (user_id, mode, materia, total, correct, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (user["id"], state["mode"], state["materia"], len(state["question_ids"]), state["corrette"], datetime.utcnow().isoformat()),
    )
    if state["mode"] == "esame":
        from ..utils import award_badge
        award_badge(db, user["id"], "primo_esame")
    db.commit()
    touch_streak(db, user["id"])
    check_quiz_badges(db, user["id"])


def _tempo_scaduto(state):
    return state.get("fine_ts") and time.time() > state["fine_ts"]


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
    formato_esame = FORMATI_ESAME.get(corpo_tag, FORMATI_ESAME[None])
    return render_template(
        "quiz/home.html", stats_generiche=stats_generiche, stats_specifiche=stats_specifiche,
        corpo_tag=corpo_tag, n_errori=n_errori, formato_esame=formato_esame,
    )


@bp.route("/avvia")
@login_required
@onboarding_required
def avvia():
    db = get_db()
    user = get_current_user()
    mode = request.args.get("mode", "practice")
    materia = request.args.get("materia") or None

    if mode == "esame":
        corpo_tag = _corpo_tag_utente(db, user["id"])
        formato = FORMATI_ESAME.get(corpo_tag, FORMATI_ESAME[None])
        domande = pick_questions_esame(db, corpo_tag, formato["n_domande"])
        if not domande:
            return redirect(url_for("quiz.home"))
        session["quiz_state"] = dict(
            mode="esame",
            materia=None,
            question_ids=[d["id"] for d in domande],
            index=0,
            corrette=0,
            punteggio=0.0,
            penalita=formato["penalita"],
            fine_ts=time.time() + formato["minuti"] * 60,
            risposte=[],
            secondi_per_domanda=None,
            in_attesa_conferma=False,
            ultimo_feedback=None,
        )
        return redirect(url_for("quiz.domanda"))

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

    if state["mode"] == "esame" and _tempo_scaduto(state):
        session["quiz_state"] = state
        _termina_sessione(db, user, state)
        return redirect(url_for("quiz.risultati"))

    if request.method == "POST":
        question_id = state["question_ids"][state["index"]]
        risposta_data = request.form.get("risposta") or None
        q = db.execute("SELECT * FROM quiz_questions WHERE id = ?", (question_id,)).fetchone()
        corretto = (risposta_data == q["risposta"])

        if risposta_data is not None:
            _aggiorna_progresso(db, user["id"], question_id, corretto)

        if state["mode"] == "esame":
            if corretto:
                state["punteggio"] += 1.0
            elif risposta_data is not None:
                state["punteggio"] -= state["penalita"]

        state["corrette"] += int(corretto)
        # Stato compatto (la sessione vive in un cookie da max ~4KB): solo id,
        # lettera data e esito. I dettagli si rileggono dal DB nei risultati.
        state["risposte"].append(dict(q=question_id, r=risposta_data, ok=int(corretto)))

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
    tempo_rimanente = None
    if state.get("fine_ts"):
        tempo_rimanente = max(0, int(state["fine_ts"] - time.time()))
    return render_template(
        "quiz/domanda.html", q=q,
        numero=state["index"] + 1, totale=len(state["question_ids"]),
        secondi=state["secondi_per_domanda"], mode=state["mode"],
        tempo_rimanente=tempo_rimanente,
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

    db = get_db()
    dettagli = []
    for r in state["risposte"]:
        q = db.execute("SELECT * FROM quiz_questions WHERE id = ?", (r["q"],)).fetchone()
        if q:
            dettagli.append(dict(
                domanda=q["domanda"], materia=q["materia"],
                risposta_data=r["r"], risposta_giusta=q["risposta"],
                corretto=bool(r["ok"]), spiegazione=q["spiegazione"],
            ))

    non_risposte = len(state["question_ids"]) - len(state["risposte"])
    return render_template(
        "quiz/risultati.html", state=state, dettagli=dettagli, non_risposte=non_risposte,
    )


@bp.route("/ripasso-ai")
@login_required
@onboarding_required
def ripasso_ai():
    db = get_db()
    user = get_current_user()
    errori = db.execute(
        """SELECT q.domanda, q.risposta, q.opzione_a, q.opzione_b, q.opzione_c, q.opzione_d, q.materia
           FROM quiz_progress p JOIN quiz_questions q ON q.id = p.question_id
           WHERE p.user_id = ? AND p.last_result = 0
           ORDER BY p.next_review ASC LIMIT 8""",
        (user["id"],),
    ).fetchall()
    return render_template(
        "quiz/ripasso_ai.html", n_errori=len(errori),
        ai_enabled=current_app.config["AI_ENABLED"],
    )


@bp.route("/ripasso-ai/genera", methods=("POST",))
@login_required
@onboarding_required
def ripasso_ai_genera():
    db = get_db()
    user = get_current_user()

    if not current_app.config["AI_ENABLED"]:
        return Response("Assistente AI non configurato in questo ambiente.", mimetype="text/plain")
    if limite_ai_raggiunto(db, user["id"]):
        return Response(
            "Hai raggiunto il limite giornaliero di messaggi per l'assistente AI. Riprova domani.",
            mimetype="text/plain",
        )

    errori = db.execute(
        """SELECT q.domanda, q.risposta, q.opzione_a, q.opzione_b, q.opzione_c, q.opzione_d, q.spiegazione, q.materia
           FROM quiz_progress p JOIN quiz_questions q ON q.id = p.question_id
           WHERE p.user_id = ? AND p.last_result = 0
           ORDER BY p.next_review ASC LIMIT 8""",
        (user["id"],),
    ).fetchall()
    if not errori:
        return Response("Non hai errori recenti da ripassare: ottimo lavoro!", mimetype="text/plain")

    blocchi = []
    for e in errori:
        opzioni = dict(A=e["opzione_a"], B=e["opzione_b"], C=e["opzione_c"], D=e["opzione_d"])
        blocchi.append(
            f"[{e['materia']}] {e['domanda']}\n"
            f"Risposta corretta: {e['risposta']}) {opzioni[e['risposta']]}\n"
            f"Nota: {e['spiegazione'] or 'nessuna'}"
        )
    prompt = "Domande sbagliate dallo studente:\n\n" + "\n\n".join(blocchi)

    # Registra la richiesta come messaggio utente così rientra nel tetto
    # giornaliero AI (il testo generato non viene salvato).
    db.execute(
        "INSERT INTO chat_messages (user_id, contesto, ruolo, contenuto, timestamp) VALUES (?, 'ripasso', 'user', ?, ?)",
        (user["id"], f"Richiesta ripasso su {len(errori)} errori", datetime.utcnow().isoformat()),
    )
    db.commit()

    api_key = current_app.config["ANTHROPIC_API_KEY"]
    messaggi = [{"role": "user", "content": prompt}]

    def genera():
        for pezzo in stream_chat(api_key, SYSTEM_PROMPT_RIPASSO, messaggi):
            yield pezzo

    return Response(stream_with_context(genera()), mimetype="text/plain")


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

    percentile = None
    righe_prec = db.execute(
        """SELECT user_id, CAST(SUM(correct_count) AS FLOAT) / SUM(attempts) AS prec
           FROM quiz_progress GROUP BY user_id HAVING SUM(attempts) >= 10""",
    ).fetchall()
    mia = next((r["prec"] for r in righe_prec if r["user_id"] == user["id"]), None)
    if mia is not None and len(righe_prec) >= 3:
        sotto = sum(1 for r in righe_prec if r["prec"] <= mia)
        percentile = round(100 * sotto / len(righe_prec))

    ultime_sessioni = db.execute(
        "SELECT * FROM quiz_sessions_log WHERE user_id = ? ORDER BY id DESC LIMIT 15",
        (user["id"],),
    ).fetchall()

    # Andamento: precisione % delle ultime 12 sessioni (dalla più vecchia), per
    # il piccolo grafico a linea nelle statistiche.
    andamento_rows = db.execute(
        """SELECT correct, total FROM quiz_sessions_log
           WHERE user_id = ? AND total > 0 ORDER BY id DESC LIMIT 12""",
        (user["id"],),
    ).fetchall()
    andamento = [round(100 * r["correct"] / r["total"]) for r in reversed(andamento_rows)]

    punti_grafico = ""
    if len(andamento) >= 2:
        larghezza, altezza = 300, 60
        passo = larghezza / (len(andamento) - 1)
        punti_grafico = " ".join(
            f"{round(i * passo)},{round(altezza - (v / 100) * altezza)}"
            for i, v in enumerate(andamento)
        )

    return render_template(
        "quiz/statistiche.html", stats_generiche=stats_generiche, stats_specifiche=stats_specifiche,
        domande_deboli=domande_deboli, n_errori=n_errori, classifica=classifica,
        percentile=percentile, ultime_sessioni=ultime_sessioni,
        andamento=andamento, punti_grafico=punti_grafico,
    )
