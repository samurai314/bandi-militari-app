import sqlite3
from pathlib import Path

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bandi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corpo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    titolo TEXT NOT NULL,
    posti TEXT,
    descrizione TEXT,
    testo_indicizzato TEXT,
    data_pubblicazione TEXT,
    data_apertura TEXT,
    data_scadenza TEXT,
    stimato INTEGER DEFAULT 0,
    fonte_url TEXT NOT NULL,
    fonte_tipo TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    bando_id INTEGER,
    sport TEXT,
    sport_anni INTEGER,
    livello TEXT,
    piegamenti INTEGER,
    trazioni INTEGER,
    corsa_distanza INTEGER,
    corsa_tempo_sec INTEGER,
    non_lo_so INTEGER DEFAULT 0,
    limitazioni TEXT,
    contesto TEXT,
    giorni_settimana INTEGER,
    onboarding_step INTEGER DEFAULT 1,
    onboarding_completed INTEGER DEFAULT 0,
    onboarding_completed_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(bando_id) REFERENCES bandi(id)
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia TEXT NOT NULL,
    domanda TEXT NOT NULL,
    opzione_a TEXT NOT NULL,
    opzione_b TEXT NOT NULL,
    opzione_c TEXT NOT NULL,
    opzione_d TEXT NOT NULL,
    risposta TEXT NOT NULL,
    spiegazione TEXT
);

CREATE TABLE IF NOT EXISTS quiz_progress (
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    repetitions INTEGER DEFAULT 0,
    interval_days INTEGER DEFAULT 0,
    ease_factor REAL DEFAULT 2.5,
    next_review TEXT,
    last_result INTEGER,
    attempts INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, question_id)
);

CREATE TABLE IF NOT EXISTS quiz_sessions_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mode TEXT NOT NULL,
    materia TEXT,
    total INTEGER,
    correct INTEGER,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS checklist_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    testo TEXT NOT NULL,
    ordine INTEGER
);

CREATE TABLE IF NOT EXISTS user_checklist (
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    checked INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, item_id)
);

CREATE TABLE IF NOT EXISTS streaks (
    user_id INTEGER PRIMARY KEY,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_date TEXT
);

CREATE TABLE IF NOT EXISTS badges (
    user_id INTEGER NOT NULL,
    codice TEXT NOT NULL,
    earned_at TEXT NOT NULL,
    PRIMARY KEY (user_id, codice)
);

CREATE TABLE IF NOT EXISTS workout_log (
    user_id INTEGER NOT NULL,
    settimana INTEGER NOT NULL,
    giorno_indice INTEGER NOT NULL,
    completato_at TEXT NOT NULL,
    PRIMARY KEY (user_id, settimana, giorno_indice)
);

CREATE TABLE IF NOT EXISTS colloquio_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    domanda TEXT NOT NULL,
    risposta TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    contesto TEXT NOT NULL,
    ruolo TEXT NOT NULL,
    contenuto TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
"""

# Colonne aggiunte dopo la prima release: le tabelle esistenti (anche già
# popolate su un deploy precedente) vengono aggiornate con ALTER TABLE,
# ignorando l'errore se la colonna esiste già (SQLite non supporta
# "ADD COLUMN IF NOT EXISTS" in modo portabile).
MIGRAZIONI = [
    "ALTER TABLE bandi ADD COLUMN stima_periodo_da TEXT",
    "ALTER TABLE bandi ADD COLUMN stima_periodo_a TEXT",
    "ALTER TABLE quiz_questions ADD COLUMN fonte TEXT DEFAULT 'originale'",
    "ALTER TABLE quiz_questions ADD COLUMN corpo_specifico TEXT",
    "ALTER TABLE profiles ADD COLUMN settimane_preferite INTEGER",
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def pulisci_markdown(testo):
    """Sostituisce il grassetto markdown (**testo**) con virgolette, dato che le
    bolle di chat mostrano il testo così com'è (senza rendering markdown)."""
    import re

    testo = re.sub(r"\*\*(.+?)\*\*", r'"\1"', testo)
    testo = re.sub(r"(?<!\*)\*(?!\*)(\S[^*\n]*?\S|\S)\*(?!\*)", r'"\1"', testo)
    return testo


def salva_messaggio_chat(db_path, user_id, contesto, ruolo, contenuto):
    """Apre una connessione indipendente da `g`: usata dentro i generator di
    streaming, dove il contesto applicativo/di richiesta potrebbe già essere
    stato chiuso quando il generator termina di produrre l'ultimo pezzo."""
    from datetime import datetime

    contenuto = pulisci_markdown(contenuto)
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO chat_messages (user_id, contesto, ruolo, contenuto, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, contesto, ruolo, contenuto, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.executescript(SCHEMA)
    for statement in MIGRAZIONI:
        try:
            conn.execute(statement)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()
    app.teardown_appcontext(close_db)
