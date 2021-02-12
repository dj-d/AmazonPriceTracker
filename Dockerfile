FROM python:3-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

WORKDIR /bot

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk add --no-cache sqlite

COPY src src
COPY credential.json .
COPY main.py .

CMD ["python", "main.py"]
