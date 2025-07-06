import time
from datetime import datetime, timedelta


class ParkingLot:

    # defining initialization - need to ensure config.toml is made and set
    def __init__(self, config, display):
        # get location from config, otherwise moondalup stn south
        self.location = config.get("location", "Moondalup Station South")

        # get total spaces from config, otherwise 500
        self.total_spaces = config.get("total_spaces", 500)

        # get temperature from config, otherwise 25 celsius
        self.temperature = float(config.get("temperature", 25.0))

        # get time from config, otherwise 9am
        self.time = config.get("time", "09:00")
        self.time = datetime.strptime(self.time, "%H:%M").time()

        self.available_spaces = self.total_spaces

        # setting variables to handle updates
        self.update_pending = False

        # saving display variable
        self.display = display

        # making dictionary variable for parked cars in format {license plate: time entered}
        self.current_cars = {}

    # defining a function to register a car entering the lot
    def enter(self, license_plate):
        license_plate = license_plate.strip()

        # needs license plate entered to function
        if not license_plate:
            print("No license plate entered.")
            return

        # same car can't park twice and leave none-ce
        if license_plate in self.current_cars:
            print("Car is already parked.")
            return


        # lower available spaces by 1
        if self.available_spaces > 0:

            self.available_spaces -= 1
            print(f"car entering parking lot - {self.available_spaces} spaces left")

            # storing parking information
            parking_time = self.time.strftime("%H:%M")
            self.current_cars[license_plate] = parking_time
            print(f"{license_plate} entered at {parking_time}")

            # pushing update
            self.update_pending = True
            self.publish_update()

        else:
            print("car entering parking lot - no spaces left")


    # defining a function to register a car leaving the lot
    def exit(self, license_plate):
        # setting variable for license plate
        license_plate = license_plate.strip()
        # if the car is already parked in the bay, cool
        if not license_plate or license_plate not in self.current_cars:
            print("wrong loicense, mate")
            return

        # increase available spaces by 1
        if self.available_spaces < self.total_spaces:
            self.available_spaces += 1

            # removes car from parked list
            del self.current_cars[license_plate]

            print(f"{license_plate} left - {self.available_spaces} spaces left")
            self.update_pending = True
            self.publish_update()

        else:
            print("no cars left in parking lot")


    # function to update temperature
    def update_temperature(self, new_temperature):
        self.temperature = new_temperature
        print(f"temperature changed to {self.temperature}")
        self.update_pending = True
        self.publish_update()

    # function to update time
    def update_time(self, new_time):
        self.time = datetime.strptime(new_time, "%H:%M").time()
        print(f"Time updated to: {self.time}")
        self.update_pending = True
        self.publish_update()

    # function to move time along (makes it look more realistic)
    def time_passing(self):
        # ticks time up by one minute
        current_datetime = datetime.combine(datetime.today(), self.time)
        new_datetime = current_datetime + timedelta(minutes=1)
        self.update_time(new_datetime.strftime("%H:%M"))


    # defining a function to publish updates on available bays, temperature and time - ALL AT ONCE
    def publish_update(self):

        if self.update_pending:

            # debug update printing
            print(f"""
                Available Bays: {self.available_spaces}
                Temperature: {self.temperature}
                Time: {self.time}
                    """)


            self.display.trigger_update()

            # turns off update-pending state
            self.update_pending = False

