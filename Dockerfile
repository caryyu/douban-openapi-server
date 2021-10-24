FROM python:3.9.4-slim

# Install packages globally
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv \
    && pipenv install --deploy --system \
    && rm -f Pipfile Pipfile.lock

# Access restriction by a non-root account
RUN useradd --create-home dos
WORKDIR /home/dos
USER dos

ADD --chown=dos:dos . /var/lib/app
ENTRYPOINT ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--chdir", "/var/lib/app", "app:app"]
