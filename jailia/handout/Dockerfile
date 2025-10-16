FROM julia:1.11.7 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY chal.jl /srv/app/run
RUN chmod 755 /srv/app/run
ENV JAIL_MEM=300M JAIL_POW=10000 JAIL_ENV_NUM=5 JAIL_CONNS_PER_IP=1 \
    JAIL_ENV_HOME=/
