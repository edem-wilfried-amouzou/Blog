#!/usr/bin/env bash
# Quitter en cas d'erreur
set -o errexit

# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Installer les dépendances Node pour DaisyUI
npm install

# 3. Compiler le CSS (DaisyUI/Tailwind)
# Assurez-vous que cette commande correspond à votre package.json
npm run build 

# 4. Collecter tous les fichiers statiques (CSS + VOS FICHIERS JS)
# Whitenoise s'occupera de les servir efficacement
python manage.py collectstatic --noinput

# 5. Appliquer les migrations sur votre base de données externe
python manage.py migrate