from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import time
class BayStatusTracker:
    """Tracks the status of each parking bay (occupied or available)."""
    def __init__(self, num_bays: int):
        self.bays = [False] * num_bays  # False = available, True = occupied

    def occupy_bay(self, bay_index: int):
        if 0 <= bay_index < len(self.bays):
            self.bays[bay_index] = True

    def free_bay(self, bay_index: int):
        if 0 <= bay_index < len(self.bays):
            self.bays[bay_index] = False

    def available_bays(self) -> int:
        return self.bays.count(False)

    def occupied_bays(self) -> int:
        return self.bays.count(True)

class MockCarparkManager(CarparkDataProvider, CarparkSensorListener):
    def __init__(self):
        self.tracker = BayStatusTracker(num_bays=1000)
        self._temperature = 22
        self._current_time = time.localtime()
        self._log_file = "carpark_activity.log"  # Add this line

    def _log_activity(self, message: str):
        with open(self._log_file, "a") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write(f"[{timestamp}] {message}\n")

    @property
    def available_spaces(self):
        return self.tracker.available_bays()

    @property
    def temperature(self):
        return self._temperature

    @property
    def current_time(self):
        return self._current_time

    def incoming_car(self, license_plate):
        for i, occupied in enumerate(self.tracker.bays):
            if not occupied:
                self.tracker.occupy_bay(i)
                self._log_activity(f"Car {license_plate} occupied bay {i}.")
                break

    def outgoing_car(self, license_plate):
        for i, occupied in enumerate(self.tracker.bays):
            if occupied:
                self.tracker.free_bay(i)
                self._log_activity(f"Car {license_plate} freed bay {i}.")
                break

    def temperature_reading(self, temp):
        self._temperature = temp
        self._current_time = time.localtime()
