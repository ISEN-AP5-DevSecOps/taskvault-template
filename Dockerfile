# [VULN] image de base lourde, non épinglée par digest, nombreuses CVE système
FROM python:3.10

# [VULN] secret dans une variable d'environnement de l'image
ENV DB_PASSWORD=P@ssw0rd2024!

# [VULN] copie de tout le contexte (y compris .git, fichiers locaux...)
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
# [VULN] le conteneur tourne en root, pas de HEALTHCHECK
CMD ["python", "app.py"]
