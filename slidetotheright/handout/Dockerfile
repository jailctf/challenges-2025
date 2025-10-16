FROM sagemath/sagemath:10.5 AS app
RUN sudo apt update
RUN sudo apt install python3 --yes

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 run.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=200M JAIL_CONNS_PER_IP=2 JAIL_PIDS=20 JAIL_CPU=200 JAIL_TIME=80 JAIL_ENV_HOME=/tmp/ JAIL_TMP_SIZE=10M
