#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Seed database
python seed_categories_authors.py
python seed_books_new.py
python seed_admin.py
python seed_users.py
