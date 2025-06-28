from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import time
import math
import string
import random

class parking_database(CarparkSensorListener, CarparkDataProvider):
    initial_empty_space = 10

    def __init__(self, update_display_callback=None):
        self._available_spaces = self.initial_empty_space
        self._temperature = 29.0  # default temperature
        self._cars_in_lot = set()
        self._update_display = update_display_callback
        
        # Update display if callback exists
        if self._update_display:
            self._update_display() 
# ------------------------------------------------------------------------------------#
# random temperature between 27-31 celcius.
# ------------------------------------------------------------------------------------#
    @property
    def temperature(self):
        time_based_value = math.sin(time.time() * 0.5)  
        self._temperature = 29 + 2 * time_based_value  
        return round(self._temperature, 1)

    @property
    def available_spaces(self) -> int:
        return self.initial_empty_space - len(self._cars_in_lot)

    # @property
    # def temperature(self) -> float:
    #     return self._temperature

    @property
    def current_time(self):
        return time.localtime()

    def temperature_reading(self, temp: float):
        print(f"[TEMP UPDATE] New temperature: {temp:.1f}°C")
        self._temperature = temp
        if self._update_display:
            self._update_display()

    def reset_parking(self):
        """reset-remove all cars."""
        print("empty spaces resetted to the initial capacity")
        self._cars_in_lot.clear()  # Remove all license plates
        if self._update_display:
            self._update_display()  # Refresh the display

# ------------------------------------------------------------------------------------#
# incomming                          #
# ------------------------------------------------------------------------------------#
#=0 new
    def incoming_car(self, license_plate: str = None):
        """Generate incomming liscence plate if input isnt provided (format: ABC-12345)"""
        if not license_plate:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            numbers = ''.join(random.choices(string.digits, k=5))
            license_plate = f"{letters}-{numbers}"
        
        # Check for duplicate plates first
        if license_plate in self._cars_in_lot:
            print(f"[WARNING] {license_plate}: has already parked")
            return
        
        # Check if parking is full (000 spaces)
        if self.available_spaces <= 0:
            print(f"[WARNING] {license_plate}: Parking is lot FULL")
            return
        
        # If all checks pass, add the car
        print(f"INCOMING vehicle. Licencse plate: {license_plate}")
        self._cars_in_lot.add(license_plate)
        
        # Check if parking just became full (was 001, now 000)
        if self.available_spaces == 0:  # After adding the car, spaces drop to 0
            print(f"[WARNING] Parking lot is now FULL (000 spaces)")
        
        if self._update_display:
            self._update_display()

# ------------------------------------------------------------------------------------#
# outgoing                          #
# ------------------------------------------------------------------------------------#
    
    def outgoing_car(self, license_plate: str):
        print(f"OUTGOING vehicle. Licencse plate: {license_plate}")
        if license_plate in self._cars_in_lot:
            self._cars_in_lot.remove(license_plate)
            if self._update_display:
                self._update_display()
        else:
            print(f"[WARNING] Unknown vehicle. License plate: {license_plate}")

