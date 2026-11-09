# TaskVault — fil rouge des TD DevSecOps (AP5)

> ⚠️ Application **volontairement vulnérable**. À utiliser uniquement en local, dans GitHub Codespaces
> ou dans un runner GitHub Actions. Ne jamais l'exposer sur Internet.

## Démarrage (TD1)

Option recommandée pour des débutants : **GitHub Codespaces** (rien à installer).

```bash
pip install -r requirements.txt -r requirements-dev.txt
python app.py            # http://localhost:5000
pytest -v
```

Comptes de test : `alice / alice123`, `bob / bob123`.

## Contenu

| Fichier | Rôle | TD |
|---|---|---|
| `app.py` | Application Flask vulnérable (SQLi, XSS/SSTI, IDOR, injection de commande, YAML, secrets…) | 1 → 6 |
| `requirements.txt` | Dépendances obsolètes (CVE connues) | 4 |
| `Dockerfile` | Image mal configurée (root, secret en ENV, image lourde) | 5 |
| `k8s/deployment.yaml` | Manifeste Kubernetes mal configuré | 5 |
| `.github/workflows/ci.yml` | Pipeline CI de départ | 1 |

## Progression du pipeline

1. **TD1** — CI : lint + tests
2. **TD2** — secrets : Gitleaks (pipeline + pre-commit)
3. **TD3** — SAST : Bandit, Semgrep (+ règle maison), SARIF
4. **TD4** — SCA : pip-audit, Trivy fs, SBOM CycloneDX, Dependabot
5. **TD5** — Conteneur & IaC : Hadolint, Trivy image, Checkov
6. **TD6** — DAST : OWASP ZAP baseline + durcissement du workflow

Le pipeline est construit pas à pas pendant les TD.
