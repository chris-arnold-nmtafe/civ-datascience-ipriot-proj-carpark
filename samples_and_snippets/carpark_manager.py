import json
import time
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
        else:
            print(f'Car entry failed: {license_plate}')
        if self.display:
            self.display.update_display()

        

    def outgoing_car(self, license_plate):
        if license_plate in self.cars:
            entry_time = self.cars.pop(license_plate)
            self._available_spaces += 1
            print(f'Car exited: {license_plate}, entered at {entry_time}')
        else:
            print(f'Car not found: {license_plate}')
        if self.display:
            self.display.update_display()

        

    def temperature_reading(self, reading):
        self._temperature = reading
        print(f'Temperature updated: {reading}°C')
        if self.display:
            self.display.update_display()

      


