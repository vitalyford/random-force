FROM python:3.8-slim

RUN apt update && apt install curl -y

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir -r requirements.txt

HEALTHCHECK --interval=1m --timeout=3s CMD curl --fail http://localhost || exit 1

ENTRYPOINT gunicorn app:app -w 4 --threads 2 -b 0.0.0.0:80
