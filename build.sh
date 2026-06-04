#!/usr/bin/env bash
# Exit on error
set -o errexit

# Installer les dépendances Node et générer le CSS
npm install
npm run build

# Installer les dépendances Python via Poetry
poetry install --no-root

# Appliquer les migrations
python manage.py collectstatic --noinput
python manage.py migrate