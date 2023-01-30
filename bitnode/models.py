"""Bitnode models."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Modes(Enum):
    """Bitcoin Operation Mode."""

    MAINNET = "mainnet"
    TESTNET = "testnet"
    REGTEST = "regtest"


class Data(BaseModel):
    core: str
    mode: Modes = Modes.MAINNET
    download_url: Optional[str] = None
    prune: Optional[int] = None
    rpc: bool = False
    user: str = "bitcoin"
