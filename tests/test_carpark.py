import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from smartpark.simple_mqtt_carpark import CarPark

class DummyClient:
    def __init__(self):
        self.published_messages = []
    def publish(self, topic, message):
        self.published_messages.append((topic, message))
    def subscribe(self, topic):
        pass
    def loop_forever(self):
        pass
    def on_message(self, a, b, c):
        pass

class TestCarPark(unittest.TestCase):
    def test_available_spaces(self):
        config = {"total-spaces": 10, "total-cars": 3}
        carpark = CarPark(config)
        carpark.client = DummyClient()  # モック化
        self.assertEqual(carpark.available_spaces, 7)


if __name__ == '__main__':
    unittest.main()