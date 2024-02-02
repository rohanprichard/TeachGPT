FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    python3-setuptools python3-dev default-libmysqlclient-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

EXPOSE 4000

CMD ["sh", "start.sh"]
