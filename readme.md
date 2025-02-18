# ereader-swedish

Upload _any_ epub book and read it in easy Swedish.

When reading normal Swedish books is too hard or/and your favorite book is not available in Swedish

## Run locally

```
 python -m venv venv
 pip install -r requirements.txt
 OPENAI_API_KEY=key  python manage.py runserver
```

## Deploy

```
set envs in fly.io console:
DJANGO_SECRET_KEY=generateyou
DB_PASSWORD=yourpassword
OPENAI_API_KEY=yourkey
PRODUCTION=true

fly deploy

```
