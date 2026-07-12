"""Punteggio di prontezza: aggrega quiz, fisico, colloquio e checklist in un
unico indicatore 0-100 con il punto più debole evidenziato.

È una stima motivazionale basata sui dati dell'app, non una previsione di
esito del concorso: la soglia di "pronto" reale la decide solo la prova vera.
"""

from datetime import date, datetime, timedelta

PESI = dict(quiz=0.40, fisico=0.30, colloquio=0.15, checklist=0.15)

ETICHETTE = dict(
    quiz="Quiz e teoria",
    fisico="Preparazione fisica",
    colloquio="Colloquio",
    checklist="Documenti",
)


def _componente_quiz(db, user_id):
    """Combina copertura (quante domande distinte hai affrontato) e precisione."""
    tot = db.execute("SELECT COUNT(*) AS c FROM quiz_questions").fetchone()["c"]
    row = db.execute(
        """SELECT COUNT(*) AS affrontate,
                  COALESCE(SUM(attempts), 0) AS tentativi,
                  COALESCE(SUM(correct_count), 0) AS corrette
           FROM quiz_progress WHERE user_id = ?""",
        (user_id,),
    ).fetchone()
    if not row["tentativi"]:
        return 0
    precisione = row["corrette"] / row["tentativi"]
    copertura = min(1.0, row["affrontate"] / max(1, tot * 0.35))
    return round(100 * (0.6 * precisione + 0.4 * copertura))


def _componente_fisico(db, user_id, totale_sessioni):
    if not totale_sessioni:
        return 0
    fatte = db.execute(
        "SELECT COUNT(*) AS c FROM workout_log WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    return round(100 * min(1.0, fatte / totale_sessioni))


def _componente_colloquio(db, user_id):
    """Considera 'allenato' chi ha scambiato almeno ~5 turni di colloquio
    e ha fatto attività di colloquio negli ultimi 14 giorni."""
    n = db.execute(
        "SELECT COUNT(*) AS c FROM chat_messages WHERE user_id = ? AND contesto = 'colloquio' AND ruolo = 'user'",
        (user_id,),
    ).fetchone()["c"]
    base = min(1.0, n / 5)
    if n:
        ultimo = db.execute(
            "SELECT MAX(timestamp) AS t FROM chat_messages WHERE user_id = ? AND contesto = 'colloquio'",
            (user_id,),
        ).fetchone()["t"]
        if ultimo and datetime.fromisoformat(ultimo) < datetime.utcnow() - timedelta(days=14):
            base *= 0.7
    return round(100 * base)


def _componente_checklist(db, user_id):
    tot = db.execute("SELECT COUNT(*) AS c FROM checklist_template").fetchone()["c"]
    if not tot:
        return 0
    fatti = db.execute(
        "SELECT COUNT(*) AS c FROM user_checklist WHERE user_id = ? AND checked = 1", (user_id,)
    ).fetchone()["c"]
    return round(100 * fatti / tot)


def calcola_prontezza(db, user_id, totale_sessioni_fisico):
    componenti = dict(
        quiz=_componente_quiz(db, user_id),
        fisico=_componente_fisico(db, user_id, totale_sessioni_fisico),
        colloquio=_componente_colloquio(db, user_id),
        checklist=_componente_checklist(db, user_id),
    )
    totale = round(sum(componenti[k] * PESI[k] for k in PESI))
    piu_debole = min(componenti, key=lambda k: componenti[k])
    return dict(
        totale=totale,
        componenti=componenti,
        etichette=ETICHETTE,
        piu_debole=piu_debole,
        piu_debole_label=ETICHETTE[piu_debole],
    )


def piano_di_oggi(db, user_id, settimana_fisico, piano):
    """Costruisce 2-3 azioni concrete per oggi in base a cosa manca."""
    azioni = []
    oggi = date.today().isoformat()

    allenato_oggi = db.execute(
        "SELECT 1 FROM workout_log WHERE user_id = ? AND completato_at LIKE ? LIMIT 1",
        (user_id, f"{oggi}%"),
    ).fetchone()
    if not allenato_oggi and piano:
        fatte_tutte = {
            (r["settimana"], r["giorno_indice"])
            for r in db.execute(
                "SELECT settimana, giorno_indice FROM workout_log WHERE user_id = ?",
                (user_id,),
            ).fetchall()
        }
        # Riparti dalla prima settimana con sessioni arretrate, non da quella
        # puramente temporale: se hai saltato, prima recuperi, poi avanzi.
        limite = min(settimana_fisico, piano["n_settimane"])
        suggerita = None
        for settimana in range(1, limite + 1):
            giorni = piano["settimane"][settimana - 1]["giorni"]
            prossimo = next(
                (i for i in range(1, len(giorni) + 1) if (settimana, i) not in fatte_tutte), None
            )
            if prossimo:
                suggerita = (settimana, prossimo, giorni[prossimo - 1]["tipo"])
                break
        if suggerita:
            settimana, prossimo, tipo = suggerita
            arretrata = " (in recupero)" if settimana < limite else ""
            azioni.append(dict(
                emoji="💪",
                testo=f"Sessione di allenamento: settimana {settimana}, giorno {prossimo} ({tipo}){arretrata}",
                url_endpoint="fisico.piano",
            ))

    materia_debole = db.execute(
        """SELECT q.materia, CAST(SUM(p.correct_count) AS FLOAT) / SUM(p.attempts) AS prec
           FROM quiz_progress p JOIN quiz_questions q ON q.id = p.question_id
           WHERE p.user_id = ? GROUP BY q.materia
           HAVING SUM(p.attempts) >= 3
           ORDER BY prec ASC LIMIT 1""",
        (user_id,),
    ).fetchone()
    if materia_debole and materia_debole["prec"] is not None and materia_debole["prec"] < 0.85:
        azioni.append(dict(
            emoji="📚",
            testo=f"10 domande di ripasso su {materia_debole['materia']} (la tua materia più debole)",
            url_endpoint="quiz.avvia",
            url_kwargs=dict(mode="practice", materia=materia_debole["materia"]),
        ))
    else:
        azioni.append(dict(
            emoji="📚",
            testo="Un quiz di prova con correzione immediata",
            url_endpoint="quiz.avvia",
            url_kwargs=dict(mode="prova"),
        ))

    una_settimana_fa = (datetime.utcnow() - timedelta(days=7)).isoformat()
    colloquio_recente = db.execute(
        """SELECT 1 FROM chat_messages
           WHERE user_id = ? AND contesto = 'colloquio' AND timestamp >= ? LIMIT 1""",
        (user_id, una_settimana_fa),
    ).fetchone()
    if not colloquio_recente:
        azioni.append(dict(
            emoji="🗣️",
            testo="Non ti alleni al colloquio da più di una settimana: fai qualche domanda",
            url_endpoint="colloquio.home",
        ))

    return azioni[:3]
