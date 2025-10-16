FROM python:3.10.12-slim-bookworm@sha256:4d440b214e447deddc0a94de23a3d97d28dfafdf125a8b4bb8073381510c9ee2 AS app
RUN pip install --no-cache-dir modelscan==0.8.6

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=80M JAIL_PIDS=30 JAIL_TMP_SIZE=1M JAIL_TIME=300 JAIL_CONNS_PER_IP=2
