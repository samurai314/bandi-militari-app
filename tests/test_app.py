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


def test_pagine_pubbliche_nuove(client):
    for percorso in ("/demo", "/scadenze", "/chi-siamo", "/privacy"):
        resp = client.get(percorso)
        assert resp.status_code == 200, percorso


def test_dashboard_mostra_prontezza_e_piano_di_oggi(client):
    registra(client, email="prontezza@test.com")
    completa_onboarding(client)
    resp = client.get("/dashboard")
    html = resp.get_data(as_text=True)
    assert "prontezza stimata" in html
    assert "Cosa fare oggi" in html


def test_teoria_indice_e_materia(client):
    registra(client, email="teoria@test.com")
    completa_onboarding(client)
    resp = client.get("/teoria/")
    assert resp.status_code == 200
    resp = client.get("/teoria/Storia")
    assert resp.status_code == 200
    resp = client.get("/teoria/MateriaInesistente")
    assert resp.status_code == 404


def test_esame_con_penalita_e_salto(client, app):
    registra(client, email="esame@test.com")
    # bando 7 = Allievi Marescialli GdF -> formato con penalità 0.25
    completa_onboarding(client, bando_id=7)

    resp = client.get("/quiz/avvia?mode=esame")
    assert resp.status_code == 302

    resp = client.get("/quiz/domanda")
    html = resp.get_data(as_text=True)
    assert "Tempo totale rimanente" in html
    assert "Salta (lascia in bianco)" in html
    token = estrai_csrf(html)

    # Salta la prima domanda (in bianco: 0 punti, nessuna penalità)
    client.post("/quiz/domanda", data=dict(csrf_token=token))

    with client.session_transaction() as sess:
        stato = sess["quiz_state"]
        assert stato["mode"] == "esame"
        assert stato["penalita"] == 0.25
        assert stato["punteggio"] == 0.0
        assert stato["risposte"][0]["r"] is None

    # Risposta sicuramente sbagliata o giusta: verifichiamo la matematica
    resp = client.get("/quiz/domanda")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/quiz/domanda", data=dict(risposta="A", csrf_token=token))

    with client.session_transaction() as sess:
        stato = sess["quiz_state"]
        atteso = 1.0 if stato["risposte"][1]["ok"] else -0.25
        assert abs(stato["punteggio"] - atteso) < 1e-9


def test_ripasso_ai_pagina(client):
    registra(client, email="ripasso@test.com")
    completa_onboarding(client)
    resp = client.get("/quiz/ripasso-ai")
    assert resp.status_code == 200


def test_soglie_fisiche_nel_piano(client):
    registra(client, email="soglie@test.com")
    completa_onboarding(client, bando_id=3)  # Marina -> soglie EMA
    resp = client.get("/fisico/")
    html = resp.get_data(as_text=True)
    assert "Il tuo divario dalle soglie" in html
    assert "Corsa 2000 m" in html


def test_registra_test_ricalibra_il_profilo(client, app):
    registra(client, email="ricalibra@test.com")
    completa_onboarding(client, bando_id=3)

    resp = client.get("/fisico/test")
    assert resp.status_code == 200
    token = estrai_csrf(resp.get_data(as_text=True))
    resp = client.post(
        "/fisico/test",
        data=dict(piegamenti=40, trazioni=10, corsa_distanza=2000,
                  corsa_tempo_sec=500, csrf_token=token),
    )
    assert resp.status_code == 302

    with app.app_context():
        from app.db import get_db
        db = get_db()
        p = db.execute(
            """SELECT p.piegamenti, p.trazioni, p.corsa_tempo_sec FROM profiles p
               JOIN users u ON u.id = p.user_id WHERE u.email = ?""",
            ("ricalibra@test.com",),
        ).fetchone()
        assert p["piegamenti"] == 40
        assert p["trazioni"] == 10
        assert p["corsa_tempo_sec"] == 500
        assert db.execute("SELECT COUNT(*) c FROM test_fisici").fetchone()["c"] >= 1

    # Con questi valori il livello deve salire da principiante a intermedio
    resp = client.get("/fisico/")
    assert "intermedio" in resp.get_data(as_text=True)


def test_settimana_test_guidato_senza_dati(client):
    registra(client, email="guidato@test.com")
    # onboarding senza dati fisici e con "non lo so"
    resp = client.get("/onboarding/step1")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step1", data=dict(bando_id=3, csrf_token=token))
    resp = client.get("/onboarding/step2")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step2", data=dict(non_lo_so=1, livello="principiante", csrf_token=token))
    resp = client.get("/onboarding/step3")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step3", data=dict(contesto="corpo_libero", giorni_settimana=4, csrf_token=token))

    resp = client.get("/fisico/")
    html = resp.get_data(as_text=True)
    assert "Test guidato" in html
    assert "australiane" in html  # variante senza sbarra per corpo libero


def test_soglie_differenziate_per_sesso(client):
    registra(client, email="soglief@test.com")
    resp = client.get("/onboarding/step1")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step1", data=dict(bando_id=3, csrf_token=token))
    resp = client.get("/onboarding/step2")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post(
        "/onboarding/step2",
        data=dict(sesso="F", piegamenti=10, trazioni=1, corsa_distanza=2000,
                  corsa_tempo_sec=700, livello="principiante", csrf_token=token),
    )
    resp = client.get("/onboarding/step3")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step3", data=dict(contesto="entrambi", giorni_settimana=4, csrf_token=token))

    resp = client.get("/fisico/")
    html = resp.get_data(as_text=True)
    assert "valori tipici donna" in html


def test_piano_include_riscaldamento_e_recupero(client):
    registra(client, email="warmup@test.com")
    completa_onboarding(client, bando_id=3)
    resp = client.get("/fisico/")
    html = resp.get_data(as_text=True)
    assert "Riscaldamento: 8-10" in html
    assert "regole d&#39;oro del recupero" in html or "regole d'oro del recupero" in html
