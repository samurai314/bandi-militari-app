from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..db import get_db
from ..fisico_engine import confronto_soglie, dati_test_mancanti, genera_piano
from ..quiz_engine import corpo_specifico_per_bando
from ..utils import get_current_user, login_required, onboarding_required, touch_streak

bp = Blueprint("fisico", __name__, url_prefix="/fisico")


@bp.route("/")
@login_required
@onboarding_required
def piano():
    db = get_db()
    user = get_current_user()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    bando = None
    if profile["bando_id"]:
        bando = db.execute("SELECT * FROM bandi WHERE id = ?", (profile["bando_id"],)).fetchone()

    data_scadenza = bando["data_scadenza"] if bando else None
    piano = genera_piano(profile, data_scadenza)

    completate_rows = db.execute(
        "SELECT settimana, giorno_indice FROM workout_log WHERE user_id = ?", (user["id"],)
    ).fetchall()
    completate = {(r["settimana"], r["giorno_indice"]) for r in completate_rows}

    totale_sessioni = sum(len(w["giorni"]) for w in piano["settimane"])

    corpo_tag = corpo_specifico_per_bando(bando["corpo"]) if bando else None
    soglie = confronto_soglie(profile, corpo_tag)

    storico_test = db.execute(
        "SELECT * FROM test_fisici WHERE user_id = ? ORDER BY data DESC LIMIT 10",
        (user["id"],),
    ).fetchall()

    return render_template(
        "fisico/piano.html", piano=piano, profile=profile, bando=bando,
        completate=completate, n_completate=len(completate), totale_sessioni=totale_sessioni,
        soglie=soglie, storico_test=storico_test,
    )


@bp.route("/test", methods=("GET", "POST"))
@login_required
@onboarding_required
def registra_test():
    db = get_db()
    user = get_current_user()
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()

    if request.method == "POST":
        campi = {}
        for nome in ("piegamenti", "trazioni", "corsa_distanza", "corsa_tempo_sec"):
            valore = request.form.get(nome, "").strip()
            campi[nome] = int(valore) if valore.isdigit() else None

        if not any(v is not None for v in campi.values()):
            flash("Inserisci almeno un valore per registrare il test.", "error")
            return redirect(url_for("fisico.registra_test"))

        db.execute(
            """INSERT INTO test_fisici (user_id, data, piegamenti, trazioni, corsa_distanza, corsa_tempo_sec, note)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user["id"], datetime.utcnow().date().isoformat(), campi["piegamenti"], campi["trazioni"],
             campi["corsa_distanza"], campi["corsa_tempo_sec"], request.form.get("note") or None),
        )

        # Ricalibrazione: i nuovi valori aggiornano il profilo, quindi livello,
        # volumi del piano e confronto soglie si ricalcolano da soli.
        aggiornamenti = {k: v for k, v in campi.items() if v is not None}
        if aggiornamenti:
            # La corsa ha senso solo in coppia distanza+tempo: aggiorna entrambe o nessuna.
            if ("corsa_distanza" in aggiornamenti) != ("corsa_tempo_sec" in aggiornamenti):
                aggiornamenti.pop("corsa_distanza", None)
                aggiornamenti.pop("corsa_tempo_sec", None)
        if aggiornamenti:
            set_clause = ", ".join(f"{k} = ?" for k in aggiornamenti)
            db.execute(
                f"UPDATE profiles SET {set_clause}, non_lo_so = 0 WHERE user_id = ?",
                (*aggiornamenti.values(), user["id"]),
            )
        from ..utils import award_badge
        award_badge(db, user["id"], "primo_test_fisico")
        db.commit()
        touch_streak(db, user["id"])
        flash("Test registrato: piano e soglie sono stati ricalibrati sui nuovi valori.", "success")
        return redirect(url_for("fisico.piano"))

    ultimo = db.execute(
        "SELECT * FROM test_fisici WHERE user_id = ? ORDER BY data DESC LIMIT 1", (user["id"],)
    ).fetchone()
    return render_template(
        "fisico/test.html", profile=profile, ultimo=ultimo,
        primo_test=dati_test_mancanti(profile),
    )


@bp.route("/completa", methods=("POST",))
@login_required
@onboarding_required
def completa():
    db = get_db()
    user = get_current_user()
    settimana = int(request.form["settimana"])
    giorno_indice = int(request.form["giorno_indice"])

    esiste = db.execute(
        "SELECT 1 FROM workout_log WHERE user_id = ? AND settimana = ? AND giorno_indice = ?",
        (user["id"], settimana, giorno_indice),
    ).fetchone()

    if esiste:
        db.execute(
            "DELETE FROM workout_log WHERE user_id = ? AND settimana = ? AND giorno_indice = ?",
            (user["id"], settimana, giorno_indice),
        )
    else:
        db.execute(
            "INSERT INTO workout_log (user_id, settimana, giorno_indice, completato_at) VALUES (?, ?, ?, ?)",
            (user["id"], settimana, giorno_indice, datetime.utcnow().isoformat()),
        )
        touch_streak(db, user["id"])

    db.commit()
    return redirect(url_for("fisico.piano") + f"#settimana-{settimana}")
