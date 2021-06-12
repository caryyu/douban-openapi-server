FROM python:3.9.4-slim

ADD . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install 

ENTRYPOINT ["pipenv", "run", "gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--access-logfile", "-", "app:app"]

