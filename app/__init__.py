import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, request, session

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _backup_giornaliero(db_path, conserva=7):
    """All'avvio, se non esiste già un backup di oggi, copia il database in
    backups/ e tiene solo gli ultimi `conserva` file. Protezione minima contro
    corruzioni o cancellazioni accidentali."""
    import shutil
    from datetime import date

    db_file = Path(db_path)
    if not db_file.exists():
        return
    cartella = db_file.parent / "backups"
    cartella.mkdir(exist_ok=True)
    destinazione = cartella / f"app-{date.today().isoformat()}.db"
    if not destinazione.exists():
        try:
            shutil.copy2(db_file, destinazione)
        except OSError:
            return
    vecchi = sorted(cartella.glob("app-*.db"))
    for f in vecchi[:-conserva]:
        try:
            f.unlink()
        except OSError:
            pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-bandi-militari")
    app.config["DATABASE"] = os.path.join(app.root_path, "..", "instance", "app.db")
    app.config["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY")
    app.config["AI_ENABLED"] = bool(app.config["ANTHROPIC_API_KEY"])
    app.config["ADMIN_EMAIL"] = os.environ.get("ADMIN_EMAIL")

    # Hardening del cookie di sessione. SESSION_COOKIE_SECURE va lasciato a
    # "false" in locale (http) e impostato a "true" nel .env di produzione
    # (PythonAnywhere serve sempre in https).
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"

    if test_config:
        app.config.update(test_config)
        app.config["AI_ENABLED"] = bool(app.config["ANTHROPIC_API_KEY"])

    from . import db
    db.init_app(app)

    with app.app_context():
        from .seed_data import seed_if_empty
        seed_if_empty()

    if not app.config.get("TESTING"):
        _backup_giornaliero(app.config["DATABASE"])

    from .routes import auth, main, onboarding, bandi, quiz, fisico, colloquio, checklist, agente, impostazioni, coach, teoria

    app.register_blueprint(teoria.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(onboarding.bp)
    app.register_blueprint(bandi.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(fisico.bp)
    app.register_blueprint(colloquio.bp)
    app.register_blueprint(checklist.bp)
    app.register_blueprint(agente.bp)
    app.register_blueprint(impostazioni.bp)
    app.register_blueprint(coach.bp)

    from .db import pulisci_markdown
    from .fisico_engine import settimane_rimanenti
    from .icons import icona_per_esercizio, video_per_esercizio
    from .utils import formatta_finestra_prevista, get_csrf_token

    app.jinja_env.filters["icona"] = icona_per_esercizio
    app.jinja_env.filters["video_esercizio"] = video_per_esercizio
    app.jinja_env.filters["settimane_rimanenti"] = settimane_rimanenti
    app.jinja_env.filters["pulisci_md"] = pulisci_markdown
    app.jinja_env.globals["finestra_prevista"] = formatta_finestra_prevista

    @app.context_processor
    def inject_helpers():
        from datetime import date, timedelta

        from .db import get_db
        from .utils import get_current_user

        user = get_current_user()
        n_scadenze = 0
        if user:
            oggi = date.today().isoformat()
            tra_3_settimane = (date.today() + timedelta(days=21)).isoformat()
            n_scadenze = get_db().execute(
                "SELECT COUNT(*) AS c FROM bandi WHERE data_scadenza BETWEEN ? AND ?",
                (oggi, tra_3_settimane),
            ).fetchone()["c"]
        return dict(
            current_user=user, csrf_token=get_csrf_token, ai_enabled=app.config["AI_ENABLED"],
            n_scadenze_imminenti=n_scadenze,
        )

    @app.before_request
    def enforce_csrf():
        if request.method == "POST":
            submitted = request.form.get("csrf_token")
            if not submitted or submitted != session.get("csrf_token"):
                abort(400, description="Token di sicurezza mancante o non valido. Ricarica la pagina e riprova.")

    return app
