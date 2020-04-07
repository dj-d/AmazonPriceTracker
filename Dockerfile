FROM python:3-alpine

COPY . /bot
WORKDIR /bot
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk add --no-cache sqlite

CMD ["python", "bot.py"]