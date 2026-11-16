# Fiche mémo Git

Toutes ces commandes se tapent dans le terminal du Codespace.

## Voir où on en est

| Commande | Rôle |
|---|---|
| `git status` | Fichiers modifiés, ajoutés, branche courante |
| `git log --oneline` | Historique des commits |
| `git diff` | Modifications pas encore ajoutées |

## Enregistrer son travail

```bash
git add app.py                  # préparer un fichier (git add . pour tout)
git commit -m "Message clair"   # enregistrer localement
git push                        # envoyer sur GitHub (déclenche le pipeline)
git pull                        # récupérer les changements de GitHub
```

## Travailler sur une branche (TD1, partie 2)

```bash
git switch -c correction-test   # créer une branche et s'y placer
# ... modifier, puis add / commit ...
git push -u origin correction-test
```

Ouvrir ensuite la pull request sur GitHub (bouton « Compare & pull request »).
Après la fusion, revenir sur main : `git switch main && git pull`.

## En cas de souci

| Situation | Commande |
|---|---|
| Annuler les modifications d'un fichier | `git restore app.py` |
| Retirer un fichier ajouté par erreur (avant commit) | `git restore --staged app.py` |
| `push` refusé : GitHub a des commits que vous n'avez pas | `git pull` puis `git push` |

⚠️ Un secret commité reste dans l'historique même après suppression du fichier (séance 2).
