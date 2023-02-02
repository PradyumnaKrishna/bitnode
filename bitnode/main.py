"""Bitnode APIs."""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Data, Modes
from template import generate_dockerfile

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.post("/generate")
def generate(data: Data):
    """Generate Dockerfile."""

    download_url = data.download_url
    known_arch = True
    if not download_url:
        known_arch = False
        download_url = f"https://bitcoincore.org/bin/bitcoin-core-{data.core}/bitcoin-{data.core}-${{TARGETPLATFORM}}.tar.gz"

    config = []
    if data.mode != Modes.MAINNET:
        config.append("# Network")
        config.append(f"{data.mode.value}=1")
        config.append("")

    if data.prune:
        config.append("# Prune the blockchain to save disk space")
        config.append(f"prune={data.prune}")
        config.append("")

    if data.rpc:
        config.append("# [rpc]")
        config.append("server=1")
        config.append("#rpcuser=")
        config.append("#rpcpassword=")
        config.append("")

    dockerfile = generate_dockerfile(
        download_url=download_url,
        user=data.user,
        known_arch=known_arch,
        copy_config=bool(config),
    )

    config = '\n'.join(config)

    return {
        "dockerfile": dockerfile,
        "config": config,
    }
