test:
	coverage run --source='apps' --omit='*/migrations/*.py,*/__init__.py,*/test*,*/apps.py' \
	manage.py test -v 2 apps && coverage html

run:
	python manage.py runserver

su:
	bash -c \
	"DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=admin \
	DJANGO_SUPERUSER_EMAIL=admin@email.fake \
	python manage.py createsuperuser --noinput"

populate_new_db:
	if [ -a db.sqlite3 ]; then rm db.sqlite3; fi
	python manage.py makemigrations
	python manage.py migrate
	make su
	python manage.py fill_ingredient_db static_files/ingredients/ingredients.csv
	python manage.py populate_db
	
	
DB_ENGINE=
DB_HOST=
DB_NAME=
DB_PORT=
POSTGRES_PASSWORD=
POSTGRES_USER=

DJANGO_ALLOWED_HOSTS=
DJANGO_SECRET_KEY=

EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_PORT=
EMAIL_TOKEN=

USER=
HOST=
SSH_KEY=
TELEGRAM_TO=
TELEGRAM_TOKEN=
DOCKER_PASSWORD=
DOCKER_USERNAME=
