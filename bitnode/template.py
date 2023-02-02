"""Template for Dockerfile and bitcoin.conf"""

from string import Template

INITIAL_DOCKERFILE = r"""FROM debian:11-slim

RUN adduser --disabled-login --gecos "" ${user}
RUN apt update && apt install curl -y
"""

DOWNLOAD_UNKNOWN_ARCH = r"""
# Download Bitcoin-Core
RUN set -ex \
    && if [ "$$(uname -m)" = "x86_64" ]; then export TARGETPLATFORM=x86_64-linux-gnu; fi \
    && if [ "$$(uname -m)" = "aarch64" ]; then export TARGETPLATFORM=aarch64-linux-gnu; fi \
    && curl -L ${download_url} -o /tmp/bitcoin.tar.gz
"""

DOWNLOAD_KNOWN_ARCH = r"""
# Download Bitcoin-Core
RUN wget -q ${download_url} -O bitcoin.tar.gz -P /tmp/
"""

INSTALL_BITCOIN = r"""
# Install Bitcoin
RUN cd /tmp && tar -xzf bitcoin.tar.gz \
    && cd $$(ls -d bitcoin*/|head -n 1) && cd bin \
    && install --mode 755 --target-directory /usr/local/bin *
"""

CREATE_CONF_DIR = r"""
# Create bitcoin.conf directory
ENV BITCOIN_DATA=/home/${user}/.bitcoin
WORKDIR /home/${user}/.bitcoin

RUN mkdir -p /home/${user}/.bitcoin
RUN chown -R ${user}:${user} /home/$user/.bitcoin
"""

COPY_CONF = r"""
# Copy bitcoin.conf
COPY bitcoin.conf /home/${user}/.bitcoin/
"""

FINAL_DOCKERFILE = r"""
# Run as user
USER ${user}

EXPOSE 8332 8333 18332 18333 18443 18444 38333 38332

CMD ["bitcoind"]
"""


def generate_dockerfile(download_url: str, user: str, **kwargs):
    """Generate Dockerfile."""

    known_arch = kwargs.get("known_arch", False)
    copy_config = kwargs.get("copy_config", False)

    dockerfile = Template(INITIAL_DOCKERFILE).substitute(user=user)
    if known_arch:
        dockerfile += Template(DOWNLOAD_KNOWN_ARCH).substitute(download_url=download_url)
    else:
        dockerfile += Template(DOWNLOAD_UNKNOWN_ARCH).substitute(download_url=download_url)

    dockerfile += Template(INSTALL_BITCOIN).substitute()
    dockerfile += Template(CREATE_CONF_DIR).substitute(user=user)

    if copy_config:
        dockerfile += Template(COPY_CONF).substitute(user=user)

    dockerfile += Template(FINAL_DOCKERFILE).substitute(user=user)

    return dockerfile
