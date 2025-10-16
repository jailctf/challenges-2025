FROM ubuntu@sha256:25895062172a2f39ae36da530f3db244b507d7ffb1c4dd42a3a487b5b446e996 AS app
RUN apt update
RUN apt-get update
RUN apt install python3 dc --yes

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/app/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=30M JAIL_PIDS=10 JAIL_TMP_SIZE=50K JAIL_TIME=30 JAIL_CONNS_PER_IP=2
