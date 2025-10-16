FROM python:3.12.9@sha256:f61c61fb2a8967599fb0874746c93530c3d2a4583478528eda06584abc736ea0 AS app
WORKDIR /app
RUN git clone --depth 1 https://github.com/ganercodes/moon ; ./moon/install

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/app/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
# warning: the proof of work may be significantly longer on remote (30000+) compared to this local distribution
ENV JAIL_MEM=300M JAIL_CPU=2500 JAIL_ENV_MOON_TMPDIR=/tmp/ JAIL_ENV_MOON_CACHEDIR=/tmp/ JAIL_PIDS=10 JAIL_POW=30000 JAIL_TIME=180 JAIL_CONNS_PER_IP=1 JAIL_TMP_SIZE=10M
