import logging
import threading
import queue
import sqlite3
from bot.connectors.hyperliquid import Hyperliquid 
from bot.connectors.vertex import Vertex 

class Position():
    def __init__(self, token: str):
        self.token = token

class ArbitrageStrategy():
    def __init__(self, private_key: str, network: str):
        self.executor_thread = None
        self.watcher_thread = None
        self.stop_event = threading.Event()
        self.hyperliquid = Hyperliquid(private_key, network)
        self.vertex = Vertex(private_key, network)
        self.positions = []
        self.positions_lock = threading.Lock()
        self.connector = sqlite3.connect("positions.db")


    def start(self):
        # TODO load positions from db
 
        # init the threads
        if not self.executor_thread:
            self.executor_thread = threading.Thread(target=self.execute, daemon=True)
            self.executor_thread.start()
            logging.debug("Started executor thread")
        else:
            logging.warning("Executor thread running already")

        if not self.watcher_thread:
            self.watcher_thread = threading.Thread(target=self.watch, daemon=True)
            self.watcher_thread.start()
            logging.debug("Started watcher thread")
        else:
            logging.warning("Watcher thread running already")

    
    def stop(self):
        self.stop_event.set()
        if self.executor_thread.is_alive():
            self.executor_thread.join()
        if self.watcher_thread.is_alive():
            self.watcher_thread.join()
        logging.debug("Shutdown completed")


    def execute(self):
        while not self.stop_event.is_set():
            pass


    def watch(self):
        while not self.stop_event.is_set():
            pass
