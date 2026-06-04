#!/usr/bin/env bash
# Quitter en cas d'erreur
set -o errexit

npm install && npm run build && pip install -r requirements.txt


# 4. Collecter tous les fichiers statiques (CSS + VOS FICHIERS JS)
# Whitenoise s'occupera de les servir efficacement
python manage.py collectstatic --noinput

# 5. Appliquer les migrations sur votre base de données externe
python manage.py migrate