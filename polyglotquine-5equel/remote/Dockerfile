# most of this setup was shamelessly stolen from the World Wide Flags CTF challenge ouroborous
# so shoutout to them (C# is actually the worst thing ever)

FROM python:alpine

RUN apk update && \
    apk add --no-cache \
    socat \
    binutils \
    nsjail \
    guile \
    nodejs \
    bash \
    nasm

RUN mkdir /dotnet-bin
RUN wget 'https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.100-rc.1.25451.107/dotnet-sdk-10.0.100-rc.1.25451.107-linux-musl-x64.tar.gz'
RUN tar zxf dotnet-sdk-10.0.100-rc.1.25451.107-linux-musl-x64.tar.gz -C /dotnet-bin
RUN rm dotnet-sdk-10.0.100-rc.1.25451.107-linux-musl-x64.tar.gz

RUN passwd -l root \
    && adduser -S -D -H -u 1000 user

WORKDIR /home/user
ENV FLAG=jail{wowowowowowow_ggs_for_pulling_this_one_off}

COPY wrapper.sh /home/user/
COPY chall_files/* /home/user/
COPY PoW-wrapper /home/user/
RUN chmod -R 555 /home/user
RUN chmod +x /home/user/PoW-wrapper

ENV POW_DIFFICULTY=100000

CMD socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:/home/user/PoW-wrapper