"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import threading
import time
import tkinter as tk
from typing import Iterable
#TODO: replace this module with yours
import mocks
import csv

# ------------------------------------------------------------------------------------#
# You don't need to understand how to implement this class.                           #
# ------------------------------------------------------------------------------------#


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, root, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Toplevel(root)
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
#        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()       
        ...
        #manager = CarparkManager(num_bays=10, weather_file='weather.csv')
       
        
        class Car:
            def __init__(self, license_plate, model, entry_time=None):
                self.license_plate = license_plate
                self.model = model
                self.entry_time = entry_time or time.strftime("%Y-%m-%d %H:%M:%S")
                self.exit_time = None
        
        class BayStatusTracker:
            def __init__(self, num_bays):
                self.bays = [False] * num_bays
        
            def occupy_bay(self):
                for i, occupied in enumerate(self.bays):
                    if not occupied:
                        self.bays[i] = True
                        return i
                return None
        
            def free_bay(self):
                for i, occupied in enumerate(self.bays):
                    if occupied:
                        self.bays[i] = False
                        return i
                return None
        
            def available_bays(self):
                return self.bays.count(False)
        
        class CarparkManager:
            def __init__(self, num_bays=10, weather_file='weather.csv'):
                self.tracker = BayStatusTracker(num_bays)
                self.cars = {}  # license_plate: Car
                self.log = []
                self.temperature = self.read_temperature(weather_file)
                self.current_time = time.localtime()
        
            def read_temperature(self, weather_file):
                try:
                    with open(weather_file, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            return float(row['temperature'])
                except Exception:
                    return 22.0  # fallback
        
            @property
            def available_spaces(self):
                return self.tracker.available_bays()
        
            def incoming_car(self, license_plate):
                model = "Unknown"  # You can extend to get model from UI
                car = Car(license_plate, model)
                self.cars[license_plate] = car
                self.tracker.occupy_bay()
                car.entry_time = time.strftime("%Y-%m-%d %H:%M:%S")
                self.log.append((license_plate, "IN", car.entry_time))
                print(f"LOG: {license_plate} entered at {car.entry_time}")
        
            def outgoing_car(self, license_plate):
                car = self.cars.get(license_plate)
                if car:
                    car.exit_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    self.tracker.free_bay()
                    self.log.append((license_plate, "OUT", car.exit_time))
                    print(f"LOG: {license_plate} exited at {car.exit_time}")
        
            def temperature_reading(self, temp):
                self.temperature = temp
        
        # Use CarparkManager in your main file instead of mocks.MockCarparkManager
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
# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self,root):
        self.window = WindowedDisplay(root,
            'Moondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()
        self._provider=None
    
    @property
    def data_provider(self):
        return self._provider
    @data_provider.setter
    def data_provider(self,provider):
        if isinstance(provider,CarparkDataProvider):
            self._provider=provider

    def update_display(self):
        field_values = dict(zip(CarParkDisplay.fields, [
            f'{self._provider.available_spaces:03d}',
            f'{self._provider.temperature:04.1f}℃',
            time.strftime("%H:%M:%S", self._provider.current_time)
        ]))
        self.window.update(field_values)

    def check_updates(self):
        while True:
            # TODO: This timer is pretty janky! Can you provide some kind of signal from your code
            # to update the display?
            time.sleep(1)
            # When you get an update, refresh the display.
            if self._provider is not None:
                self.update_display()


class CarDetectorWindow:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, root):
        self.root = root
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50),
            cursor='right_side', command=self.incoming_car
        )
        self.btn_incoming_car.grid(padx=10, pady=5, row=0, columnspan=2)

        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘', font=('Arial', 50),
            cursor='bottom_left_corner', command=self.outgoing_car
        )
        self.btn_outgoing_car.grid(padx=10, pady=5, row=1, columnspan=2)

        self.listeners = list()

        self.temp_label = tk.Label(
            self.root, text="Temperature", font=('Arial', 20)
        )
        self.temp_label.grid(padx=10, pady=5, column=0, row=2)

        self.temp_var = tk.StringVar()
        self.temp_var.trace_add(
            "write",
            lambda *args: self.temperature_changed(self.safe_float(self.temp_var.get()))
        )
        self.temp_box = tk.Entry(
            self.root, font=('Arial', 20), textvariable=self.temp_var
        )
        self.temp_box.grid(padx=10, pady=5, column=1, row=2)

        self.plate_label = tk.Label(
            self.root, text="License Plate", font=('Arial', 20)
        )
        self.plate_label.grid(padx=10, pady=5, column=0, row=3)

        self.plate_var = tk.StringVar()
        self.plate_box = tk.Entry(
            self.root, font=('Arial', 20), textvariable=self.plate_var
        )
        self.plate_box.grid(padx=10, pady=5, column=1, row=3)

        self.display = None  # Will be set externally

    @staticmethod
    def safe_float(value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    @property
    def current_license(self):
        return self.plate_var.get()

    def add_listener(self, listener):
        if isinstance(listener, CarparkSensorListener):
            self.listeners.append(listener)

    def incoming_car(self):
        for listener in self.listeners:
            listener.incoming_car(self.current_license)

    def outgoing_car(self):
        for listener in self.listeners:
            listener.outgoing_car(self.current_license)

    def temperature_changed(self, temp):
        for listener in self.listeners:
            listener.temperature_reading(temp)
        # Update display immediately if available
        if self.display is not None:
            self.display.update_display()


if __name__ == '__main__':
    root = tk.Tk()

    mock = mocks.MockCarparkManager()
    display = CarParkDisplay(root)
    display.data_provider = mock

    detector = CarDetectorWindow(root)
    detector.add_listener(mock)
    detector.display = display  # Allow detector to update display

    root.mainloop()
