# ereader-swedish

Upload _any_ epub book and read it in easy Swedish.

When reading normal Swedish books is too hard or/and your favorite book is not available in Swedish

<img width="813" alt="image" src="https://github.com/user-attachments/assets/482cc15e-61db-4e69-9f6c-ced2f241ab3d" />


[https://ereader-swedish.fly.dev/](https://ereader-swedish.fly.dev/)

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
