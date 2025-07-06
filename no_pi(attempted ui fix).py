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
from tkinter import scrolledtext



# ------------------------------------------------------------------------------------#
# You don't need to understand how to implement this class.                           #
# ------------------------------------------------------------------------------------#


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'


#TODO: i know i wasn't meant to touch the display but i figured i could try making it look nicer


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
        self.window.geometry('800x600')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create label for field name, left-aligned, font size 30
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 30), anchor='w')
            # create label for value, left-aligned, font size 30
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 30), anchor='w')

            # position the elements in 2 columns, both left aligned
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky='w', padx=10, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=1, sticky='w', padx=10, pady=5)


        # writing a header line for parked cars
        parked_header_row = len(display_fields)
        self.gui_elements['lbl_parked_header'] = tk.Label(
            self.window, text="Currently Parked Cars (License Plate - Arrival Time):", font=('Arial', 20, 'bold'), anchor='w')
        self.gui_elements['lbl_parked_header'].grid(
            row=parked_header_row, column=0, sticky='w', padx=10, pady=(20, 0), columnspan=2)

        # listing all parked cars in a SCROLLABLE textbox
        self.gui_elements['txt_parked_list'] = scrolledtext.ScrolledText(
            self.window, width=60, height=10, font=('Arial', 16), wrap='none', state='disabled')
        self.gui_elements['txt_parked_list'].grid(
            row=parked_header_row + 1, column=0, columnspan=2, sticky='w', padx=10, pady=5)

    def show(self):
        """Display the GUI. Blocking call."""
        # self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for i, field in enumerate(self.display_fields):
            value_label = self.gui_elements.get(f'lbl_value_{i}')
            if value_label:
                value_label.configure(
                    text=updated_values.get(field, self.DISPLAY_INIT)
                )
        self.window.update()

        # update parked car list if it's not empty
        parked_text = updated_values.get('__parked__')
        if parked_text is not None:
            text_widget = self.gui_elements['txt_parked_list']
            text_widget.config(state='normal')
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, parked_text)
            text_widget.config(state='disabled')


# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""


    def __init__(self,root, parking_lot, config):
        # creating an instance variable of config to handle easier
        self.config = config

        # determines what fields appear in the UI
        self.fields = [f"{self.config['location']}", 'Available bays', 'Temperature', 'Current Time']

        # creating a threading event for updating
        self._update_event = threading.Event()

        # this bit initializes the window for display
        self.window = WindowedDisplay(root, 'Moondalup', self.fields)

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
        field_values = dict(zip(self.fields, [
            f"(Capacity: {self.config['total_spaces']})",
            f'{self._provider.available_spaces:}',
            f'{self._provider.temperature:.1f}℃',
            self._provider.time.strftime("%H:%M")
        ]))

        # show all parked cars
        parked_text = "\n".join(
            f"{plate} — {entry_time}" for plate, entry_time in self._provider.current_cars.items()
        ) or "None"
        field_values["__parked__"] = parked_text

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

        # car enters button
        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Car Entering', font=('Arial', 50), cursor='right_side', command=self.incoming_car, bg="green", fg="white")
        self.btn_incoming_car.grid(padx=10, pady=5,row=0,columnspan=2)

        # car exits button
        self.btn_outgoing_car = tk.Button(
            self.root, text='Car Exiting 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car, bg="red", fg="white")
        self.btn_outgoing_car.grid(padx=10, pady=5,row=1,columnspan=2)
        self.listeners=list()

        self.temp_label=tk.Label(
            self.root, text="Temperature", font=('Arial', 20)
        )

        # disabling the temperature bar in lieu of having buttons - temperature can be manually adjusted by increments of 0.1°C
        """ 
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

        # license plate input
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
        # getting license plate variable
        license_plate = self.current_license.strip().upper()

        if not license_plate:
            print("need a plate there, mate")
            return
        self.parking_lot.enter(license_plate)

    def outgoing_car(self):
        # getting license plate variable
        license_plate = self.current_license.strip().upper()

        if not license_plate:
            print("need a plate there, mate")
            return
        self.parking_lot.exit(license_plate)

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
