import logging
import eth_account
from eth_account.signers.local import LocalAccount
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

class Hyperliquid():
    def __init__(self, private_key: str, network: str):
        logging.debug("Setting up hyperliquid connection...")

        self.private_key = private_key
        self.account: LocalAccount = eth_account.Account.from_key(self.private_key)
        if network == "mainnet":
            self.net = constants.MAINNET_API_URL
        else:
            self.net = constants.TESTNET_API_URL

        self.info = Info(self.net, skip_ws=True)
        self.exchange = Exchange(self.account, self.net)
        logging.debug("OK")


    def get_user_state(self):
        user_state = self.info.user_state(self.private_key)
        logging.debug(user_state)


    def order(self):
        order_result = self.exchange.order("ETH", True, 0.2, 1100, {"limit": {"tif": "Gtc"}})
        if order_result["status"] == "ok":
                status = order_result["response"]["data"]["statuses"][0]
                if "resting" in status:
                    order_status = self.info.query_order_by_oid(self.account.address, status["resting"]["oid"])
                    logging.debug("Order status by oid:", order_status)
