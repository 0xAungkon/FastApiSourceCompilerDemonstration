# Backend-Core

Deployment:
make migrate
python manage.py makemigrations common && python manage.py migrate common
make create-admin

Docker Clear:
docker compose up -d --build --force-recreate