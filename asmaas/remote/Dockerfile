FROM python:3.13.7@sha256:c1dab8c06c4fe756fd4316f33a2ba4497be09fa106d2cd9782c33ee411193f9c AS app
RUN pip install --no-cache-dir pwntools

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY asm.py /srv/app/run
RUN chmod 755 /srv/app/run
ENV JAIL_MEM=60M JAIL_TMP_SIZE=1M JAIL_PIDS=10 JAIL_CONNS_PER_IP=2 \
    JAIL_ENV_PATH=/usr/local/bin:/usr/bin:/bin
