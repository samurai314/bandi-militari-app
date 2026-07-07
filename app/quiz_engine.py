"""Spaced repetition semplificata (variante di SM-2) per il ripasso quiz."""

from datetime import date, timedelta


def review(repetitions, interval_days, ease_factor, correct):
    """Calcola il nuovo stato di ripetizione dopo una risposta.

    quality alto (5) se corretta, basso (2) se sbagliata: non chiediamo
    all'utente un giudizio di difficoltà per restare semplici da usare.
    """
    quality = 5 if correct else 2

    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(1.3, ease_factor)

    if not correct:
        repetitions = 0
        interval_days = 1
    else:
        repetitions += 1
        if repetitions == 1:
            interval_days = 1
        elif repetitions == 2:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)

    next_review = date.today() + timedelta(days=interval_days)
    return repetitions, interval_days, ease_factor, next_review.isoformat()


def pick_questions(db, user_id, materia=None, limit=10, mode="practice"):
    """Sceglie le domande per una sessione.

    - practice: priorità alle domande in scadenza di ripasso (spaced repetition),
      poi alle domande mai fatte, filtrate per materia se indicata.
    - timed/simulation: selezione ampia e mescolata tra le materie.
    """
    today = date.today().isoformat()

    if mode == "practice":
        materia_filter = "AND q.materia = ?" if materia else ""

        due = db.execute(
            f"""SELECT q.* FROM quiz_questions q
                JOIN quiz_progress p ON p.question_id = q.id AND p.user_id = ?
                WHERE p.next_review <= ? {materia_filter}
                ORDER BY p.next_review ASC""",
            [user_id, today] + ([materia] if materia else []),
        ).fetchall()

        new_filter = "AND materia = ?" if materia else ""
        new_params = [user_id] + ([materia] if materia else [])
        new_qs = db.execute(
            f"""SELECT * FROM quiz_questions
                WHERE id NOT IN (SELECT question_id FROM quiz_progress WHERE user_id = ?)
                {new_filter}""",
            new_params,
        ).fetchall()

        combined = list(due) + list(new_qs)
        return combined[:limit]

    # timed / simulation: mix ampio, ordine casuale lato SQL
    return db.execute(
        "SELECT * FROM quiz_questions ORDER BY RANDOM() LIMIT ?", (limit,)
    ).fetchall()


def materia_stats(db, user_id):
    rows = db.execute(
        """SELECT q.materia,
                  COUNT(*) AS totale,
                  SUM(CASE WHEN p.correct_count > 0 THEN 1 ELSE 0 END) AS con_almeno_una_corretta,
                  COALESCE(SUM(p.attempts), 0) AS tentativi,
                  COALESCE(SUM(p.correct_count), 0) AS corrette
           FROM quiz_questions q
           LEFT JOIN quiz_progress p ON p.question_id = q.id AND p.user_id = ?
           GROUP BY q.materia""",
        (user_id,),
    ).fetchall()
    stats = []
    for r in rows:
        tentativi = r["tentativi"] or 0
        corrette = r["corrette"] or 0
        pct = round(100 * corrette / tentativi) if tentativi else None
        stats.append(
            dict(materia=r["materia"], totale=r["totale"], tentativi=tentativi,
                 corrette=corrette, percentuale=pct)
        )
    return stats
