import app as taskvault


def client():
    taskvault.init_db()
    taskvault.app.config["TESTING"] = True
    return taskvault.app.test_client()


def test_health():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_index():
    r = client().get("/")
    assert r.status_code == 200
    assert b"TaskVault" in r.data


def test_login_ok():
    r = client().post("/login", data={"username": "alice", "password": "alice123"})
    assert r.status_code == 302


def test_login_ko():
    r = client().post("/login", data={"username": "alice", "password": "mauvais"})
    assert r.status_code == 401
