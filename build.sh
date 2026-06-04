#!/usr/bin/env bash
set -o errexit

# 1. Installer les dépendances Node et build le CSS
npm install
npm run build

# 2. Installer les dépendances Python via pip (la méthode standard)
pip install -r requirements.txt

# 3. Migrations et statics
python manage.py collectstatic --noinput
python manage.py migrate