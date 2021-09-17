# Foodgram Продуктовый помощник

![Foodgram Workflow Status](https://github.com/ynmatveev/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg?branch=main&event=push)

### Описание


Foodgram – это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
- python 3.8.9
- django 3.2.2
- django rest framework 3.12.4
- PostgreSQL 12.4
- nginx 1.19.3
- docker

### Необходимые приложения
В проекте предусмотрена выгрузка списка покупок в pdf файл.
Чтобы эта функция работала, необходимо установить в систему WKHTMLTOPDF([Установить](https://wkhtmltopdf.org/downloads.html))):


### Запуск приложения

Для запуска приложения вам потребуется установить git ([Установка git](https://git-scm.com/book/ru/v2/Введение-Установка-Git))  и docker ([Установка docker](https://www.docker.com/get-started)) на ваш компьютер.


Склонируйте приложение из репозитория на GitHUB. Для этого в терминале перейдите в директорию, в которую хотите скопировать приложение и выполните команду:

```bash
git clone https://github.com/YNMatveev/foodgram-project
```

Из корневой директории проекта (там где находится файл **manage.py**) и
выполните в терминале команду:

```bash
docker-compose up -d
```

Докер соберет необходимые образы и запустит контейнеры в фоновом режиме.

Далее можно подготовить базу данных вручную, либо запустить makefile

### Подготовка базы данных вручную

Для подготовки базы данных в терминале выполните команды:
```bash
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
```

### Создание суперпользователя и доступ к админке
Для создания суперпользователя в терминале выполните команду (заменив username, you_password и admin@email.fake на нужные):

```bash
docker-compose exec web bash -c \
"DJANGO_SUPERUSER_USERNAME=your_username \
DJANGO_SUPERUSER_PASSWORD=your_password \
DJANGO_SUPERUSER_EMAIL=admin@email.fake \
python manage.py createsuperuser --noinput"
```
или с вводом нужных вам данных в терминале

```bash
docker-compose exec web python manage.py createsuperuser
```
### Подготовка статики

Чтобы собрать всю статику проекта, выполните:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Наполнение БД начальными данными

```bash
docker-compose exec web python manage.py fill_ingredient_db static_files/ingredients/ingredients.csv
docker-compose exec web python manage.py populate_db
```

Теперь можно зайти в админку по адресу:
[http://localhost/admin/](http://localhost/admin/) или [http://127.0.0.1/admin/](http://127.0.0.1/admin/)


### Подготовка и наполнение БД начальными данными c помощью makefile

Для тестирования работы проекта можно подготовить и наполнить базу данных тестовыми данными.
В корневой папке приложения подготовлен makefile.

Для этого в терминале выполните команду:

```bash
docker-compose exec web make first_time_prepare
```

После запуска команды будут выполнены:
- подготовка файлов миграции
- миграция базы данных
- создан суперпользователь с логином "admin", паролем "admin" и адресом электронной почты "admin@email.fake"
- из файла static_files/ingredients/ingredients.csv загружены данные в модель Ingredient
- остальные данные (пользователи, рецепты, подписки и пр.) будут сгенерированы случайным образом
- у всех сгенерированных пользователей будет пароль "secret"
