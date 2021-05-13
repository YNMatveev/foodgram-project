test:
	coverage run --source='apps' --omit='*/migrations/*.py,*/__init__.py,*/test*,*/apps.py' \
	manage.py test -v 2 apps && coverage html

run:
	python manage.py runserver