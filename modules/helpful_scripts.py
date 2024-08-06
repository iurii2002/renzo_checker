import datetime
from sys import stderr
from pathlib import Path
from typing import List

from loguru import logger
from web3 import Account
from eth_account.signers.local import LocalAccount

from config import log_file


def load_logger():
    # LOGGING SETTING
    logger.remove()
    logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")
    logger.add(log_file + f"_{datetime.datetime.now().strftime('%Y%m%d')}.log",
               format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")
    logger.opt(ansi=True)


def load_accounts_from_keys(path: str) -> List[LocalAccount]:
    file = Path(path).open()
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def load_wallets(path: str) -> List[str]:
    file = Path(path).open()
    return [line.replace("\n", "") for line in file.readlines()]


class MakePause(BaseException):
    def __init__(self, timer: int = None):
        self.timer = timer
