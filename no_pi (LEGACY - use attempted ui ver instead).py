"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
import parkinglot
from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
import threading
import time
import tkinter as tk
from typing import Iterable
import tomli
#TODO: replace this module with yours
from parkinglot import ParkingLot



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

# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ["Location", 'Available bays', 'Temperature', 'Current Time']

    def __init__(self,root, parking_lot, config):
        # creating an instance variable of config to handle easier
        self.config = config

        # creating a threading event for updating
        self._update_event = threading.Event()

        # this bit initializes the window for display
        self.window = WindowedDisplay(root,
            'Moondalup', CarParkDisplay.fields)

        # this part starts the background part for checking for updates
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()


        self.window.show()

        self._provider= parking_lot
        self.parking_lot = parking_lot


    @property
    def data_provider(self):
        return self._provider
    @data_provider.setter
    def data_provider(self,provider):
        if isinstance(provider,ParkingLot):
            self._provider=provider

    def update_display(self):
        field_values = dict(zip(CarParkDisplay.fields, [
            f"Location:{self.config['location']} | Capacity: {self.config['total_spaces']}",
            f'{self._provider.available_spaces:}',
            f'{self._provider.temperature:.1f}℃',
            self._provider.time.strftime("%H:%M")
        ]))
        self.window.update(field_values)

    # this was painful but parkinglot.py should notify an update should happen and then no_pi should run the update
    def check_updates(self):
        while True:


            # blocking events until triggered
            self._update_event.wait()

            # updates display
            self.update_display()

            # clears event to wait for next update
            self._update_event.clear()



    def trigger_update(self):
        # manually setting events to trigger
        self._update_event.set()


    # making a dinky little definition to simulate time passing
    def time_ticker(self):
        # loading the time passing function
        self._provider.time_passing()

        # calls for update
        self.trigger_update()

        # scheduling a minute per 3 seconds real-time should be good - THIS IS THE NEXT TICK SO IT GOES **AFTER** THE UPDATE
        self.window.window.after(3000, self.time_ticker)


class CarDetectorWindow:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, root, parking_lot):
        self.root=root
        self.root.title("Car Detector ULTRA")

        # new instance of parkinglot to handle cars entering and exiting
        self.parking_lot = parking_lot


        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Car Entering', font=('Arial', 50), cursor='right_side', command=self.parking_lot.enter, bg="green", fg="white")
        self.btn_incoming_car.grid(padx=10, pady=5,row=0,columnspan=2)

        self.btn_outgoing_car = tk.Button(
            self.root, text='Car Exiting 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.parking_lot.exit, bg="red", fg="white")
        self.btn_outgoing_car.grid(padx=10, pady=5,row=1,columnspan=2)
        self.listeners=list()

        self.temp_label=tk.Label(
            self.root, text="Temperature", font=('Arial', 20)
        )

        """ disabling this in place of buttons
        self.temp_label.grid(padx=10, pady=5,column=0,row=2)
        self.temp_var=tk.StringVar()
        self.temp_var.trace_add("write",lambda x,y,v: self.temperature_changed(float(self.temp_var.get())))
        self.temp_box=tk.Entry(
            self.root,font=('Arial', 20),textvariable=self.temp_var
        )
        self.temp_box.grid(padx=10, pady=5,column=1,row=2)
        """

        # blue decrease temperature button
        self.temp_down = tk.Button(
            self.root,
            text = "-0.1°C",
            font = ("Arial", 20),
            fg = "blue",
            command=lambda: self.adjust_temperature(-0.1)
        )
        self.temp_down.grid(padx=10, pady=5, column=0, row=4)

        # red increase temperature button
        self.temp_up = tk.Button(
            self.root,
            text = "+0.1°C",
            font = ("Arial", 20),
            fg = "red",
            command=lambda: self.adjust_temperature(+0.1)
        )
        self.temp_up.grid(padx=10, pady=5, column=1, row=4)
        self.plate_label=tk.Label(
            self.root, text="License Plate", font=('Arial', 20)
        )
        self.plate_label.grid(padx=10, pady=5,column=0,row=3)
        self.plate_var=tk.StringVar()
        self.plate_box=tk.Entry(
            self.root,font=('Arial', 20),textvariable=self.plate_var
        )
        self.plate_box.grid(padx=10, pady=5,column=1,row=3)

    @property
    def current_license(self):
        return self.plate_var.get()

    def add_listener(self,listener):
        if isinstance(listener,CarparkSensorListener):
            self.listeners.append(listener)

    def incoming_car(self):
#        print("Car goes in")
        for listener in self.listeners:
            listener.incoming_car(self.current_license)

    def outgoing_car(self):
#        print("Car goes out")
        for listener in self.listeners:
            listener.outgoing_car(self.current_license)

    def temperature_changed(self,temp):
        for listener in self.listeners:
            listener.temperature_reading(temp)


    # fandangling this took way too long
    def adjust_temperature(self, delta):
        # get temperature from parking lot
        current_temp = self.parking_lot.temperature


        # sets new temperature based on deltas from buttons
        new_temp = round(current_temp + delta, 1)

        # notify the gui window to display the temperature change
        self.parking_lot.update_temperature(new_temp)


if __name__ == '__main__':
    root = tk.Tk()

    # read config file
    with open("config.txt", "r") as file:
        config_string = file.read()

    # parse the configuration
    config = tomli.loads(config_string)

    # creating parkinglot instance
    parking_lot_instance = ParkingLot(config, display=None)


    # initializing CarParkDisplay
    display=CarParkDisplay(root, parking_lot_instance, config)

    """
  pain and suffering, i forgot to update parkinglot.display
  this took me too long to realise
     """
    # setting carpark display
    parking_lot_instance.display = display


    display.data_provider=parking_lot_instance

    # running the ticker to simulate time passing
    display.time_ticker()

    # initializing CarDetectorWindow
    detector=CarDetectorWindow(root, parking_lot_instance)
    detector.add_listener(parking_lot_instance)



    root.mainloop()
