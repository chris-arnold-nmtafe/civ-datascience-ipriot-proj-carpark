from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import time

class MockCarparkManager(CarparkSensorListener,CarparkDataProvider):
    @property
    def available_spaces(self):
        return 1000

    @property
    def temperature(self):
        return 1000

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self,license_plate):
        print('Car in! ' + license_plate)

    def outgoing_car(self,license_plate):
        print('Car out! ' + license_plate)

    def temperature_reading(self,reading):
        print(f'temperature is {reading}')
