import logging
from hyperliquid.info import Info
from hyperliquid.utils import constants


class Hyperliquid():
    def __init__(self, private_key: str, network: str):
        self.private_key = private_key
        if network == "mainnet":
            self.net = constants.MAINNET_API_URL
        else:
            self.net = constants.TESTNET_API_URL

        logging.debug("Setting up hyperliquid connection...")
        self.info = Info(self.net, skip_ws=True)
        logging.debug("OK")


    def get_user_state(self):
        user_state = self.info.user_state(self.private_key)
        logging.debug(user_state)
