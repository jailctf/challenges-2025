FROM rust@sha256:fcbb950e8fa0de7f8ada015ea78e97ad09fcc4120bf23485664e418e0ec5087b AS app
RUN apt update
RUN apt install python3 --yes

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=100M JAIL_PIDS=70 JAIL_TIME=60 JAIL_CONNS_PER_IP=2 JAIL_TMP_SIZE=50M
