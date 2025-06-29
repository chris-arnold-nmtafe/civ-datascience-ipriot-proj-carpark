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
        # for temperature 
        self._temperature = 27.0  
        ##NOTE: uncomment for self changing feature
        # self._step=0
        # self._trig_variable = random.uniform(0, 2*math.pi)
        #
        self._cars_in_lot = set()
        self._update_display = update_display_callback
        
        if self._update_display:
            self._update_display() 
# ------------------------------------------------------------------------------------#
# Math function to make temperature flactuate between 27-31 celcius.
# ------------------------------------------------------------------------------------#
    @property
    ##NOTE:equation for self changing temperature. Uncomment for self changing feature
    # def temperature(self):              
    #         self._step += 1
    #         if self._step % 50 < 25:
    #             base_change = 0.16
    #         else:
    #             base_change = -0.16
    #         maf_function_one = math.sin(self._step/5 + self._trig_variable) * 0.08              #equation derived from chat GPT
    #         self._temperature = min(max(27, self._temperature + base_change + maf_function_one), 31)
    #         return round(self._temperature, 1)
    #NOTE:manual temperature input
    def temperature(self) -> float:
        return self._temperature
    

    @property
    def available_spaces(self) -> int:
        return self.initial_empty_space - len(self._cars_in_lot)

    @property
    def current_time(self):
        return time.localtime()

    def temperature_reading(self, temp: float):
        print(f"[TEMP UPDATE] New temperature: {temp:.1f}°C")
        self._temperature = temp
        if self._update_display:
            self._update_display()

# ------------------------------------------------------------------------------------#
# reset                          #
# ------------------------------------------------------------------------------------#         

    def reset_parking(self):
        """reset-remove all cars."""
        print("empty spaces resetted to the initial capacity")
        self._cars_in_lot.clear()  
        if self._update_display:
            self._update_display()  

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
        
        # duplicate check
        if license_plate in self._cars_in_lot:
            print(f"[WARNING] {license_plate}: has already parked")
            return
        
        if self.available_spaces <= 0:
            print(f"[WARNING] {license_plate}: Parking is lot FULL")
            return
        
        print(f"INCOMING vehicle. Licencse plate: {license_plate}")
        
        self._cars_in_lot.add(license_plate)
        if self.available_spaces == 0:  
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

