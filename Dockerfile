FROM python:3-alpine

COPY requirements.txt /bot/
WORKDIR /bot

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN apk add --no-cache sqlite

COPY .  /bot

CMD ["python", "bot.py"]
