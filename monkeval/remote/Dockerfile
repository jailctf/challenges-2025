FROM rakudo-star:2025.04 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY chal.raku /srv/app/run
RUN chmod 755 /srv/app/run
RUN mv /srv/app/flag.txt /srv/app/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=200M JAIL_PIDS=10 JAIL_TIME=50 JAIL_CONNS_PER_IP=2
