FROM ubuntu:24.04 AS app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y \
    wget \
    software-properties-common \
    ca-certificates \
    guile-3.0 \
    nodejs \
    nasm \
    python3 \
    binutils

RUN mkdir /dotnet-bin
RUN wget 'https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.100-rc.1.25451.107/dotnet-sdk-10.0.100-rc.1.25451.107-linux-x64.tar.gz'
RUN tar zxf dotnet-sdk-10.0.100-rc.1.25451.107-linux-x64.tar.gz -C /dotnet-bin
RUN rm dotnet-sdk-10.0.100-rc.1.25451.107-linux-x64.tar.gz
ENV DOTNET_ROOT=/dotnet-bin

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]