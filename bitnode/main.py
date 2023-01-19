from enum import Enum
from string import Template
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from template import SAMPLE_DOCKERFILE, REGTEST_CONFIG

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Modes(Enum):
    """Bitcoin Operation Mode."""

    MAINNET = "mainnet"
    TESTNET = "testnet"
    REGTEST = "regtest"


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "dockerfile": SAMPLE_DOCKERFILE},
    )


@app.get("/generate")
def generate(
    request: Request,
    core: str,
    mode: Modes,
    download_url: Optional[str] = None,
    user: str = "bitcoin",
):
    """Generate Dockerfile."""

    if mode == Modes.REGTEST:
        config = REGTEST_CONFIG
    else:
        config = ""

    if not download_url:
        download_url = f"https://bitcoincore.org/bin/bitcoin-core-{core}/bitcoin-{core}-${{TARGETPLATFORM}}.tar.gz"

    dockerfile = Template(SAMPLE_DOCKERFILE).substitute(
        user=user, download_url=download_url
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "dockerfile": dockerfile, "config": config},
    )
