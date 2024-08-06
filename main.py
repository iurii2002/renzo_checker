import random
import time
from loguru import logger

from modules.helpful_scripts import load_logger, load_wallets
from modules.renzo_sdk import RenzoSDK
from config import wallets_file, sleep_between_accounts


def main_script():
    wallets = load_wallets(wallets_file)

    logger.info(f"Started for {len(wallets)} accounts")
    if len(wallets) == 0:
        logger.error(f'Add wallets to {wallets_file} file')
        return

    for address in wallets:

        load_logger()
        random_sleep = random.randint(*sleep_between_accounts)

        try:
            sdk = RenzoSDK(address=address)
            sdk.check_airdrop_season_2()
        except ConnectionError as err:
            logger.info(f'ConnectionError: {err}')
            random_sleep *= 3
        except ValueError as value:
            logger.info(f'ValueError: {value}')
            random_sleep *= 3
        except Exception as err:
            logger.error(f'Something went wrong with account {address} : {err}')
            random_sleep *= 3

        time.sleep(random_sleep)


if __name__ == "__main__":
    main_script()
