FROM python:3.10.2 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY chal.py /srv/app/run
RUN chmod 755 /srv/app/run
# pow is longer on remote btw
ENV JAIL_POW=100 JAIL_MEM=50M JAIL_TIME=90 JAIL_CONNS_PER_IP=2
