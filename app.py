"""
TaskVault - application VOLONTAIREMENT VULNÉRABLE pour le module DevSecOps (AP5).
NE JAMAIS DÉPLOYER EN PRODUCTION NI SUR UN SERVEUR EXPOSÉ.

Vulnérabilités volontaires (à trouver pendant les TD) :
  - injection SQL, injection de commande, XSS (SSTI), IDOR,
  - secrets en dur, mode debug, hachage faible, désérialisation YAML non sûre,
  - dépendances obsolètes (requirements.txt), Dockerfile et manifeste K8s mal configurés.
"""
import hashlib
import os
import sqlite3
import subprocess

import yaml
from flask import Flask, request, session, redirect, render_template_string, g

app = Flask(__name__)

# [VULN] secrets codés en dur dans le code source
app.secret_key = "super-secret-key-123"
api_key = "a8f5f167f44f4964e6c998dee827110c4b2e9a7d"

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taskvault.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def hash_password(password):
    # [VULN] MD5 sans sel : hachage faible
    return hashlib.md5(password.encode()).hexdigest()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS tasks;
        CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
        CREATE TABLE tasks (id INTEGER PRIMARY KEY, owner_id INTEGER, title TEXT, secret_note TEXT);
        """
    )
    db.execute("INSERT INTO users VALUES (1, 'alice', ?)", (hash_password("alice123"),))
    db.execute("INSERT INTO users VALUES (2, 'bob', ?)", (hash_password("bob123"),))
    db.execute("INSERT INTO tasks VALUES (1, 1, 'Préparer la démo', 'code wifi : 1234')")
    db.execute("INSERT INTO tasks VALUES (2, 2, 'Payer les impôts', 'IBAN FR76 0000 0000 0000')")
    db.commit()
    db.close()


PAGE = """
<!doctype html><title>TaskVault</title>
<h1>TaskVault</h1>
<p>{{ message }}</p>
<form method="post" action="/login">
  <input name="username" placeholder="utilisateur">
  <input name="password" type="password" placeholder="mot de passe">
  <button>Connexion</button>
</form>
<form action="/search"><input name="q" placeholder="rechercher"><button>OK</button></form>
"""


@app.route("/")
def index():
    user = session.get("user", "invité")
    return render_template_string(PAGE, message="Bonjour " + user)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    # [VULN] injection SQL : la requête est construite par concaténation
    query = (
        "SELECT * FROM users WHERE username = '" + username
        + "' AND password = '" + hash_password(password) + "'"
    )
    user = get_db().execute(query).fetchone()
    if user:
        session["user"] = user["username"]
        session["user_id"] = user["id"]
        return redirect("/")
    return render_template_string(PAGE, message="Identifiants invalides"), 401


@app.route("/search")
def search():
    q = request.args.get("q", "")
    # [VULN] XSS / injection de template (SSTI) : l'entrée utilisateur est insérée dans le template
    return render_template_string("<h2>Résultats pour : " + q + "</h2>")


@app.route("/task/<int:task_id>")
def task(task_id):
    # [VULN] IDOR : aucune vérification que la tâche appartient à l'utilisateur connecté
    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return {"error": "introuvable"}, 404
    return dict(row)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # [VULN] injection de commande : shell=True avec une entrée utilisateur
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return "<pre>" + output.decode(errors="ignore") + "</pre>"


@app.route("/import", methods=["POST"])
def import_config():
    # [VULN] désérialisation non sûre (yaml.load sans SafeLoader)
    data = yaml.load(request.data, Loader=yaml.Loader)
    return {"imported": str(data)}


if __name__ == "__main__":
    init_db()
    # [VULN] mode debug activé et écoute sur toutes les interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
