FROM python:3.8-slim-buster

RUN apt update && apt install wkhtmltopdf make -y

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000