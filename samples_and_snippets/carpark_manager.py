import json
import time
import os
from interfaces import CarparkSensorListener, CarparkDataProvider

class CarparkManager(CarparkSensorListener, CarparkDataProvider):

    def __init__(self, config_file='samples_and_snippets/config.json'):
        with open(config_file, 'r') as file:
            data = json.load(file)
        
        carpark = data['CarParks'][0]
        self.name = carpark['name']
        self.max_spaces = carpark['total-spaces']

        self._available_spaces = self.max_spaces
        self._temperature = 0
        self.cars = {}  
        self.display = None

        if not os.path.exists('logs'):
            os.makedirs('logs')

    def set_display(self, display):
        self.display = display

    @property
    def available_spaces(self):
        return self._available_spaces

    @property
    def temperature(self):
        return self._temperature

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self, license_plate):
        if self._available_spaces > 0 and license_plate not in self.cars:
            self.cars[license_plate] = time.strftime("%H:%M:%S")
            self._available_spaces -= 1
            print(f'Car entered: {license_plate} at {self.cars[license_plate]}')
            self.log_event(f'IN  - {license_plate} at {self.cars[license_plate]}')
        else:
            print(f'Car entry failed: {license_plate}')
            self.log_event(f'IN FAILED - {license_plate}')
        if self.display:
            self.display.update_display()

        

    def outgoing_car(self, license_plate):
        if license_plate in self.cars:
            entry_time = self.cars.pop(license_plate)
            self._available_spaces += 1
            print(f'Car exited: {license_plate}, entered at {entry_time}')
            self.log_event(f'OUT - {license_plate} entered at {entry_time}')
        else:
            print(f'Car not found: {license_plate}')
            self.log_event(f'OUT FAILED - {license_plate}')
        if self.display:
            self.display.update_display()

        

    def temperature_reading(self, reading):
        self._temperature = reading
        print(f'Temperature updated: {reading}°C')
        self.log_event(f'Temperature set to {reading}°C')
        if self.display:
            self.display.update_display()

    def log_event(self, message):
        with open('logs/car_log.txt', 'a') as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f'{timestamp} - {message}\n')

      


