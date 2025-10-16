FROM python:3.12 AS app
RUN apt update && apt upgrade --yes
RUN git clone https://github.com/battlecode/battlecode25-scaffold /battlecode25-scaffold
WORKDIR /battlecode25-scaffold/python
RUN python3 /battlecode25-scaffold/python/run.py update
RUN chmod -R 777 /battlecode25-scaffold

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=300M JAIL_PIDS=20 JAIL_TIME=300 JAIL_CONNS_PER_IP=2 JAIL_TMP_SIZE=500M

