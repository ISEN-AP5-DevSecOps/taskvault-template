FROM mcr.microsoft.com/devcontainers/python:1-3.10-bookworm

# Le dépôt apt de Yarn fourni par l'image a une clé GPG expirée :
# apt-get update échoue et bloque l'installation de Docker (feature docker-in-docker).
RUN grep -rl yarnpkg /etc/apt/sources.list.d/ | xargs -r rm -f
