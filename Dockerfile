FROM python:3.6-slim
RUN apt-get update && apt-get upgrade -y && apt-get install libpq-dev gcc -y
ADD requirements.txt requirements.txt
ADD manage.py manage.py
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT python manage.py runserver 0.0.0.0:80
