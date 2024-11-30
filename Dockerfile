FROM python:3.11.7
MAINTAINER Fahad Najib <choudharyfahad@gmail.com>

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
ADD . .

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 80

CMD [ "gunicorn", "gunicorn_app:app", "--workers", "1", "--worker-class", "gevent", "--worker-connections", "1000", "-b", "0.0.0.0:80", "--timeout", "200", "--log-level", "debug", "--access-logfile", "-" ]
