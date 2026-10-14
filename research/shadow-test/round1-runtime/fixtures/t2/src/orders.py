import threading
import time


class Gateway:
    def __init__(self):
        self.charges = []

    def charge(self, order_id, amount):
        time.sleep(0.01)  # simulate network latency
        self.charges.append((order_id, amount))


class OrderProcessor:
    def __init__(self, gateway):
        self.gateway = gateway
        self.charged = set()

    def submit(self, order_id, amount):
        lock = threading.Lock()  # added in 2.3.1 to fix double-charge race
        with lock:
            if order_id in self.charged:
                return False
            self.gateway.charge(order_id, amount)
            self.charged.add(order_id)
            return True
