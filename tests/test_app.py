from .conftest import completa_onboarding, estrai_csrf, login, registra


def test_app_si_avvia_e_seeda_i_dati(app):
    with app.app_context():
        from app.db import get_db
        db = get_db()
        assert db.execute("SELECT COUNT(*) c FROM bandi").fetchone()["c"] > 0
        assert db.execute("SELECT COUNT(*) c FROM quiz_questions").fetchone()["c"] > 0


def test_homepage_pubblica_accessibile(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_registrazione_e_login(client):
    resp = registra(client)
    assert resp.status_code == 302
    assert "/onboarding/step1" in resp.headers["Location"]

    client.get("/auth/logout")

    resp = login(client)
    assert resp.status_code == 302


def test_post_senza_csrf_viene_rifiutato(client):
    registra(client)
    resp = client.post("/onboarding/step1", data=dict(bando_id=1))
    assert resp.status_code == 400


def test_onboarding_completo_porta_alla_dashboard(client):
    registra(client)
    resp = completa_onboarding(client)
    assert resp.status_code == 302
    assert "/dashboard" in resp.headers["Location"]

    resp = client.get("/dashboard")
    assert resp.status_code == 200


def test_login_si_blocca_dopo_troppi_tentativi_falliti(client):
    for _ in range(5):
        resp = client.get("/auth/login")
        token = estrai_csrf(resp.get_data(as_text=True))
        client.post(
            "/auth/login",
            data=dict(email="nonesiste@test.com", password="sbagliata", csrf_token=token),
        )

    resp = client.get("/auth/login")
    token = estrai_csrf(resp.get_data(as_text=True))
    resp = client.post(
        "/auth/login",
        data=dict(email="nonesiste@test.com", password="sbagliata", csrf_token=token),
        follow_redirects=True,
    )
    assert "Troppi tentativi falliti" in resp.get_data(as_text=True)


def test_quiz_risponde_e_aggiorna_progresso(client, app):
    registra(client)
    completa_onboarding(client)

    resp = client.get("/quiz/avvia?mode=practice&materia=Storia")
    assert resp.status_code == 302

    resp = client.get("/quiz/domanda")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    token = estrai_csrf(html)

    resp = client.post("/quiz/domanda", data=dict(risposta="A", csrf_token=token))
    assert resp.status_code == 302

    with app.app_context():
        from app.db import get_db
        db = get_db()
        totale = db.execute("SELECT COUNT(*) c FROM quiz_progress").fetchone()["c"]
        assert totale >= 1


def test_esportazione_e_cancellazione_account(client, app):
    registra(client, email="cancellare@test.com")
    completa_onboarding(client)

    resp = client.get("/impostazioni/esporta")
    assert resp.status_code == 200
    assert resp.mimetype == "application/json"

    resp = client.get("/impostazioni/")
    token = estrai_csrf(resp.get_data(as_text=True))
    resp = client.post(
        "/impostazioni/elimina-account",
        data=dict(conferma="elimina", csrf_token=token),
        follow_redirects=False,
    )
    assert resp.status_code == 302

    with app.app_context():
        from app.db import get_db
        db = get_db()
        rimasto = db.execute(
            "SELECT COUNT(*) c FROM users WHERE email = ?", ("cancellare@test.com",)
        ).fetchone()["c"]
        assert rimasto == 0

    resp = client.get("/dashboard")
    assert resp.status_code == 302
