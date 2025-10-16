FROM node:18.9.1 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 index.js /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=90M JAIL_CPU=300 JAIL_TMP_SIZE=10M JAIL_PIDS=20 JAIL_TIME=30 JAIL_CONNS_PER_IP=2
