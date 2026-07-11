import os
import re
import tempfile

import pytest

from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    application = create_app(dict(
        DATABASE=db_path,
        SECRET_KEY="test-secret-key",
        ANTHROPIC_API_KEY=None,
        TESTING=True,
    ))
    yield application
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def estrai_csrf(html):
    match = re.search(r'name="csrf_token" value="([^"]*)"', html)
    assert match, "csrf_token non trovato nella pagina"
    return match.group(1)


def registra(client, email="utente@test.com", password="password123"):
    resp = client.get("/auth/register")
    token = estrai_csrf(resp.get_data(as_text=True))
    return client.post(
        "/auth/register",
        data=dict(email=email, password=password, csrf_token=token),
        follow_redirects=False,
    )


def login(client, email="utente@test.com", password="password123"):
    resp = client.get("/auth/login")
    token = estrai_csrf(resp.get_data(as_text=True))
    return client.post(
        "/auth/login",
        data=dict(email=email, password=password, csrf_token=token),
        follow_redirects=False,
    )


def completa_onboarding(client, bando_id=1):
    resp = client.get("/onboarding/step1")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post("/onboarding/step1", data=dict(bando_id=bando_id, csrf_token=token))

    resp = client.get("/onboarding/step2")
    token = estrai_csrf(resp.get_data(as_text=True))
    client.post(
        "/onboarding/step2",
        data=dict(
            piegamenti=15, trazioni=3, corsa_distanza=2000, corsa_tempo_sec=600,
            livello="principiante", csrf_token=token,
        ),
    )

    resp = client.get("/onboarding/step3")
    token = estrai_csrf(resp.get_data(as_text=True))
    return client.post(
        "/onboarding/step3",
        data=dict(contesto="entrambi", giorni_settimana=4, csrf_token=token),
    )
