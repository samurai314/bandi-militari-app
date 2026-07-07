import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-bandi-militari")
    app.config["DATABASE"] = os.path.join(app.root_path, "..", "instance", "app.db")

    from . import db
    db.init_app(app)

    with app.app_context():
        from .seed_data import seed_if_empty
        seed_if_empty()

    from .routes import auth, main, onboarding, bandi, quiz, fisico, colloquio, checklist, agente

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(onboarding.bp)
    app.register_blueprint(bandi.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(fisico.bp)
    app.register_blueprint(colloquio.bp)
    app.register_blueprint(checklist.bp)
    app.register_blueprint(agente.bp)

    @app.context_processor
    def inject_helpers():
        from .utils import get_current_user
        return dict(current_user=get_current_user())

    return app
