FROM python:3.13.7@sha256:c1dab8c06c4fe756fd4316f33a2ba4497be09fa106d2cd9782c33ee411193f9c AS app
RUN apt-get update && apt-get install -y nodejs
RUN pip install --no-cache-dir bfi

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY main.py /srv/app/run
RUN chmod 755 /srv/app/run
ENV JAIL_MEM=80M JAIL_PIDS=10 JAIL_CONNS_PER_IP=2
