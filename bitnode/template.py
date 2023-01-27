"""Template for Dockerfile and bitcoin.conf"""

SAMPLE_DOCKERFILE = r"""FROM debian:11-slim

RUN adduser --disabled-login --gecos "" ${user}
RUN apt update && apt install wget -y

RUN set -ex \
    && if [ "$$(uname -m)" = "x86_64" ]; then export TARGETPLATFORM=x86_64-linux-gnu; fi \
    && if [ "$$(uname -m)" = "aarch64" ]; then export TARGETPLATFORM=aarch64-linux-gnu; fi \
    wget -q ${download_url} -O bitcoin.tar.gz \
    && tar -xzf bitcoin.tar.gz \
    && cd $$(ls -d bitcoin*/|head -n 1) && cd bin \
    && install --mode 755 --target-directory /usr/local/bin *

ENV BITCOIN_DATA=/home/${user}/.bitcoin
WORKDIR /home/${user}/.bitcoin

COPY bitcoin.conf /home/${user}/.bitcoin/
RUN chown -R ${user}:${user} /home/$user/.bitcoin

USER ${user}

EXPOSE 8332 8333 18332 18333 18443 18444 38333 38332

CMD ["bitcoind"]
"""
