from datetime import datetime
import json
import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces}, "
                + "TEMPC: 42"
            )
        )
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + "TEMPC: 42"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()
        print(f"🚗 entered → total cars: {self.total_cars}")

    def on_car_exit(self):
        if self.total_cars > 0:
            self.total_cars -= 1
        self._publish_event()
        print(f"🚗 exited → total cars: {self.total_cars}")


    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
    
        try:
            data = json.loads(payload)
            action = data.get("action", "").lower()
            self.temperature = int(data.get("temperature", 0))
        except ValueError:
            print("⚠️ Error: Could not parse temperature from payload:", payload)
            return

        if 'exit' in action.lower():
            self.on_car_exit()
        else:
            self.on_car_entry()



from config_parser import parse_config

if __name__ == '__main__':
    config = parse_config("config.toml")
    print("✔ config loaded:", config)  
    car_park = CarPark(config)
    print("Carpark initialized")

