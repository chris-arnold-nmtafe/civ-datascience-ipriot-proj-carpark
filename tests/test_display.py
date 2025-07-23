import unittest
from smartpark.simple_mqtt_display import Display

class DummyClient:
    def __init__(self):
        self.published = []

    def connect(self, *args, **kwargs):
        pass  # 接続しない

    def loop_start(self):
        pass  # ループしない

    def subscribe(self, topic):
        pass

    def publish(self, topic, message):
        self.published.append((topic, message))


class TestDisplay(unittest.TestCase):
    def test_display_initialization(self):
        
        config = {
            'name': 'display',
            'location': 'L306',
            'topic-root': 'lot',
            'broker': 'localhost',
            'port': 1883,
            'topic-qualifier': 'na'
        }

        try:
            display = Display(config)
            display.client = DummyClient()  # 実接続を避ける
            self.assertIsInstance(display, Display)
            
        except Exception as e:
            self.fail(f"Display init failed: {e}")

if __name__ == '__main__':
    unittest.main()
