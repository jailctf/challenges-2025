FROM python:3.13.5@sha256:4ea77121eab13d9e71f2783d7505f5655b25bb7b2c263e8020aae3b555dbc0b2 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=27M JAIL_TIME=300 JAIL_CONNS_PER_IP=2 JAIL_TMP_SIZE=5M
