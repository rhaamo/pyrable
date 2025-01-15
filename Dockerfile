FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DOWNLOAD_CACHE=/noop/

WORKDIR /app

COPY . .

RUN \
    echo 'installing dependencies' && \
    apk add --no-cache \
    python3-dev \
    py3-psycopg2 \
    py3-pip \
    py3-virtualenv

RUN \
    echo 'installing pip requirements' && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install setuptools wheel && \
    /venv/bin/pip install -r /app/requirements.txt && \
    rm -rf $PIP_DOWNLOAD_CACHE

EXPOSE 443

VOLUME /ssl

CMD ["/venv/bin/flask", "run", "-h", "0.0.0.0", "-p", "443", "--cert=/ssl/cert.pem", "--key=/ssl/key.pem"]