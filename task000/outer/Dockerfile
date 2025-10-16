FROM python:3.13.5@sha256:4ea77121eab13d9e71f2783d7505f5655b25bb7b2c263e8020aae3b555dbc0b2 AS app

RUN apt update
RUN apt install curl socat netcat-traditional -y

WORKDIR /app
COPY ./main.py /app/main.py
COPY ./flag.txt /app/flag.txt
COPY ./task000.json /app/task000.json

ENTRYPOINT ["socat", "-t", "15", "tcp-l:17000,reuseaddr,fork", "EXEC:\"python3 main.py\",stderr,pty,echo=0"]

