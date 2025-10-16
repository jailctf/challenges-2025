FROM python:3.12 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=27M JAIL_TIME=30 JAIL_CONNS_PER_IP=2
