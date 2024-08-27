FROM python:3.11.7-slim-bullseye

RUN apt-get update && \
    apt-get install -y git
    
WORKDIR /opt/app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /opt/app

EXPOSE ${PORT}

RUN chown www-data:www-data -R /opt/app

USER www-data

WORKDIR /opt/

CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT}