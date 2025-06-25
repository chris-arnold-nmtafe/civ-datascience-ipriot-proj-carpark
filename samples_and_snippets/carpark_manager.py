import time
from interfaces import CarparkSensorListener, CarparkDataProvider

class CarparkManager(CarparkSensorListener, CarparkDataProvider):

    def __init__(self):
        self._max_spaces = 10
        self._cars = {}  
        self._temperature = 0.0 
    
    @property
    def available_spaces(self):
        return self._max_spaces - len(self._cars)

    @property
    def temperature(self):
        return self._temperature

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self, license_plate):
        if self.available_spaces > 0 and license_plate not in self._cars:
            self._cars[license_plate] = time.strftime("%H:%M:%S")
            print(f'Car entered: {license_plate} at {self._cars[license_plate]}')
        else:
            print(f'Car entry failed: {license_plate}')
        

    def outgoing_car(self, license_plate):
        if license_plate in self._cars:
            entry_time = self._cars.pop(license_plate)
            print(f'Car exited: {license_plate}, entered at {entry_time}')
        else:
            print(f'Car not found: {license_plate}')
        

    def temperature_reading(self, reading):
        self._temperature = reading
        print(f'Temperature updated: {reading}°C')
      


