import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, request, session

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-bandi-militari")
    app.config["DATABASE"] = os.path.join(app.root_path, "..", "instance", "app.db")
    app.config["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY")
    app.config["AI_ENABLED"] = bool(app.config["ANTHROPIC_API_KEY"])

    from . import db
    db.init_app(app)

    with app.app_context():
        from .seed_data import seed_if_empty
        seed_if_empty()

    from .routes import auth, main, onboarding, bandi, quiz, fisico, colloquio, checklist, agente, impostazioni

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

    from .utils import get_csrf_token

    @app.context_processor
    def inject_helpers():
        from .utils import get_current_user
        return dict(current_user=get_current_user(), csrf_token=get_csrf_token, ai_enabled=app.config["AI_ENABLED"])

    @app.before_request
    def enforce_csrf():
        if request.method == "POST":
            submitted = request.form.get("csrf_token")
            if not submitted or submitted != session.get("csrf_token"):
                abort(400, description="Token di sicurezza mancante o non valido. Ricarica la pagina e riprova.")

    return app
