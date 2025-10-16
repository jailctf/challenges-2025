FROM python:3.13.5@sha256:4ea77121eab13d9e71f2783d7505f5655b25bb7b2c263e8020aae3b555dbc0b2 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 flag_lottery.py /srv/app/run
COPY --chmod=755 lottery_machine.py /srv/app/lottery_machine.py
ENV JAIL_CPU=100 JAIL_MEM=25M JAIL_TIME=7777 JAIL_CONNS_PER_IP=10 JAIL_TMP_SIZE=5M
