"""Bitnode APIs."""

from string import Template
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Data, Modes
from template import SAMPLE_DOCKERFILE

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "dockerfile": SAMPLE_DOCKERFILE},
    )


@app.post("/generate")
def generate(data: Data):
    """Generate Dockerfile."""

    download_url = data.download_url
    if not download_url:
        download_url = f"https://bitcoincore.org/bin/bitcoin-core-{data.core}/bitcoin-{data.core}-${{TARGETPLATFORM}}.tar.gz"

    dockerfile = Template(SAMPLE_DOCKERFILE).substitute(
        user=data.user, download_url=download_url,
    )

    config = []
    if data.mode != Modes.MAINNET:
        config.append("# Network")
        config.append(f"{data.mode.value}=1")
        config.append("")

    if data.prune:
        config.append("# Prune the blockchain to save disk space")
        config.append(f"prune={data.prune}")
        config.append("")

    config = '\n'.join(config)

    return {
        "dockerfile": dockerfile,
        "config": config,
    }
