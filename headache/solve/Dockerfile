FROM ubuntu:questing@sha256:36bbb8adc0662496d3e314bc8a25cb41c0c2e42ed25daaa07f8369d36d16f082 AS app

RUN apt update
RUN apt upgrade --yes
RUN apt install git make flex bison --yes
RUN apt install build-essential --yes

RUN git clone https://github.com/LucasMW/Headache /app/Headache/
WORKDIR /app/Headache/
# this line below is a hack to get it compiling on docker idk why it doesnt compile on docker properly
RUN sed -i "s|CFLAGS = -Wall -std=c99 -O3|CFLAGS = -Wall -std=gnu99 -O3|g" Makefile
# the line above is not a key detail in solving this challenge
RUN make

RUN git clone https://github.com/TheFoxan12/BrainfuckInterpreter /app/BrainfuckInterpreter/
WORKDIR /app/BrainfuckInterpreter/
RUN gcc main.c -o interpreter

RUN apt install python3 --yes

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chall.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=35M JAIL_PIDS=15 JAIL_CPU=150 JAIL_TIME=50 JAIL_CONNS_PER_IP=2 JAIL_TMP_SIZE=15M

