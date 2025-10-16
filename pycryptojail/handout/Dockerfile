FROM python:3.12.4@sha256:e8be0ea148390d08bc077840cf87ac6a538d80b0ea1e8752b3e3982987cd0a53 AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY flag.txt /srv/app/flag.txt
COPY chal.py /srv/app/run
RUN chmod 755 /srv/app/run
ENV JAIL_MEM=30M JAIL_TIME=60 JAIL_CONNS_PER_IP=2
