FROM python@sha256:4d440b214e447deddc0a94de23a3d97d28dfafdf125a8b4bb8073381510c9ee2 AS app
RUN apt-get update && apt-get install g++ gdb binutils binutils-gold --yes

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chall.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=100M JAIL_PIDS=14 JAIL_TIME=60 JAIL_CONNS_PER_IP=2 JAIL_CPU=150 JAIL_TMP_SIZE=10M
