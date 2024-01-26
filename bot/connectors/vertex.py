import logging
from vertex_protocol.client import create_vertex_client
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce

class Vertex():
    def __init__(self, private_key: str, network: str):
        logging.debug("Setting up vertex connection...")
        self.private_key = private_key
        self.network = network
        self.client = create_vertex_client(self.network, self.private_key)
        logging.debug("OK")
