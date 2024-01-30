import time
import json
import logging
import os
from bot.strategies.arbitrage import ArbitrageStrategy

logging.basicConfig(level=logging.DEBUG)

def main():
    strategy = None
    try:
        private_key = os.environ.get('PRIVATE_KEY')
        network = os.environ.get('NETWORK')
        strategy = ArbitrageStrategy(private_key, network)
        strategy.start()
    except KeyboardInterrupt:
        logging.debug("Interrupt received, stopping...")
    finally:
        if strategy:
            strategy.stop()
            logging.debug("OK")

if __name__ == "__main__":
    main()
