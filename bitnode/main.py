"""Bitnode CLI"""

import os
from enum import Enum
from string import Template

import typer

from bitnode.templates.dockerfile import SAMPLE_DOCKERFILE, REGTEST_CONFIG

cli = typer.Typer()


class Modes(Enum):
    """Modes to run bitcoind"""

    REGTEST = "regtest"


@cli.command()
def generate(
    url: str = typer.Argument(..., help="bitcoin-core download url"),
    mode: Modes = typer.Argument(..., help="bitcoind run mode", case_sensitive=False),
    user: str = typer.Option("bitcoin", help="docker user")
):
    """Generates Dockerfile and config for bitcoin-nodes."""
    print("Generating Dockerfile and config...")

    # generate dockerfile
    dockerfile = Template(SAMPLE_DOCKERFILE).substitute(
        download_url=url, user=user
    )

    # generate config
    conf = None
    if mode == Modes.REGTEST:
        conf = REGTEST_CONFIG

    # export files
    os.makedirs("output", exist_ok=True)
    with open("output/Dockerfile", "w", encoding="UTF-8") as file:
        file.write(dockerfile)
    if conf:
        with open("output/bitcoin.conf", "w", encoding="UTF-8") as file:
            file.write(conf)

    print("Dockerfile and config generated at output folder.")
