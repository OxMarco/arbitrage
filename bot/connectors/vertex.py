import time
import logging
from vertex_protocol.client import create_vertex_client
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams,
    SubaccountParams
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce


class Vertex():
    def __init__(self, private_key: str, network: str):
        logging.debug("Setting up vertex connection...")
        self.private_key = private_key
        if network == 'testnet':
            self.network = 'sepolia-testnet'
        else:
            self.network = network
        self.client = create_vertex_client(self.network, self.private_key)
        logging.debug("OK")


    def place_order(self, amount):
        token_allowance = self.client.spot.get_token_allowance(0, self.client.context.signer.address)
        if token_allowance < amount:
            approve_allowance_tx_hash = self.client.spot.approve_allowance(0, amount)
            logging.debug(f"Approve tx {approve_allowance_tx_hash}")
        
        deposit_tx_hash = self.client.spot.deposit(
            DepositCollateralParams(
                subaccount_name="default", product_id=0, amount=amount
            )
        )
        logging.info(f"Tx hash: {deposit_tx_hash}")
        owner = self.client.context.engine_client.signer.address
        product_id = 1
        order = OrderParams(
            sender=SubaccountParams(
                subaccount_owner=owner,
                subaccount_name="default",
            ),
            priceX18=to_x18(20000),
            amount=to_pow_10(1, 17),
            expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
            nonce=gen_order_nonce(),
        )
        order = self.client.market.place_order({"product_id": product_id, "order": order})
        logging.info(order)
