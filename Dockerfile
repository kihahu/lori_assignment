FROM python:3.6-slim
RUN apt-get update && apt-get upgrade -y && apt-get install libpq-dev gcc -y
ADD . .
RUN rm -rf terraform
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ./entrypoint.sh